import sys
from calculator.constants import (
    TUBE_TYPES, 
    COEFFICIENTS_LESS_EQUAL_200, 
    COEFFICIENTS_GREATER_200, 
    COEFFICIENTS_1_5_T, 
    FITTING_PARAMETERS,
    FITTING_PARAMETERS_1_5_T, 
    LENGTH_MULTIPLIERS
)
from calculator.utils import mm_to_inch, inch_to_mm

class BaseElement:
    def __init__(self, diameter, element_type, magnet_type):
        self.diameter = round(diameter, 1)
        self.element_type = element_type
        if element_type not in TUBE_TYPES:
            #! not working
            raise ValueError(f"Element type '{element_type}' is not supported. Choose from {TUBE_TYPES}.")

    def calculate_pressure(self, previous_pressure_drop, length_so_far, n):
        raise NotImplementedError("Subclasses should implement this method")

class Element(BaseElement):
    def __init__(self, diameter, length=0, angle=None, type=None, element_type=None, magnet_type=None):
        if angle and type:
            element_type = f"{angle}° {type}"
            if angle not in [45, 90]:
                raise ValueError("Only 45 and 90 degree elbows are supported")
            if type not in ["segmented", "smooth", "mitred"]:
                raise ValueError("Elbow type must be 'segmented', 'smooth', or 'mitred'")
        self.diameter = diameter
        self.length = length
        self.angle = angle
        self.type = type
        self.magnet_type = magnet_type
        self.element_type = element_type or "straight"

    def calculate_pressure(self, previous_pressure_drop, length_so_far, n):
        length_multiplier = LENGTH_MULTIPLIERS
        lenght = (self.length * length_multiplier[self.element_type][1] + self.diameter / 127 * length_multiplier[self.element_type][0])
        self.length = lenght

        P1_mbar = previous_pressure_drop
        P1_pa = P1_mbar * 100
        diameter_mm = self.diameter  # diameter in millimeters

        if self.magnet_type == 1:
            fitting_params = FITTING_PARAMETERS_1_5_T['smooth']  # default fitting parameters
            if self.element_type == "straight flexible":
                fitting_params = FITTING_PARAMETERS_1_5_T['flexible']
        else:
            fitting_params = FITTING_PARAMETERS['smooth']  # default fitting parameters
            if self.element_type == "straight flexible":
                fitting_params = FITTING_PARAMETERS['flexible']

        P_prime = ((P1_pa) * (diameter_mm * 0.001) ** fitting_params['P1']) ** fitting_params['P2']
        L_prime = self.get_L_prime(P_prime)
        P_L_prime = self.get_P_L_prime(L_prime)
        P_L_prime_plus_L = self.get_P_L_prime_plus_L(L_prime)
        dP = P_L_prime_plus_L - P_L_prime
        element_pressure_drop = dP / 100

        # print(f"diameter = {mm_to_inch(diameter_mm)} inch ({diameter_mm} mm))")
        # print(f"length = {self.length} m")
        # print(f"element type = {self.element_type}")
        # print("fitting_params['P2'] = ", fitting_params['P2'])
        # print("fitting_params['P1'] = ", fitting_params['P1'])
        # print("P1_pa = ", P1_pa)
        # print("P1_mbar = ", P1_mbar)
        # print("P_prime = ", P_prime)
        # print("L_prime = ", L_prime)
        # print("P(L') = ", P_L_prime)
        # print("P(L'+L) = ", P_L_prime_plus_L)
        # print("dP = P(L'+L)-P(L') = ", dP)
        # print("element pressure drop = ", element_pressure_drop)
        # print("-----------------------------")

        return element_pressure_drop

    def get_L_prime(self, P_prime):
        if self.magnet_type == 1:
            coefficients = COEFFICIENTS_1_5_T
        else:
            coefficients = COEFFICIENTS_LESS_EQUAL_200 if P_prime <= 29 else COEFFICIENTS_GREATER_200
        index = 3 if self.element_type == "straight flexible" else 2

        L_prime = (((((coefficients['6th order'][index] * P_prime + coefficients['5th order'][index]) * P_prime + coefficients['4th order'][index]) * P_prime + coefficients['3rd order'][index]) * P_prime + coefficients['2nd order'][index]) * P_prime + coefficients['1st order'][index]) * P_prime

        return L_prime

    def get_P_L_prime(self, L_prime):
        if self.magnet_type == 1:
            coefficients = COEFFICIENTS_1_5_T
            fitting_params = FITTING_PARAMETERS_1_5_T['flexible'] if self.element_type == "straight flexible" else FITTING_PARAMETERS_1_5_T['smooth']
        else:
            coefficients = COEFFICIENTS_LESS_EQUAL_200 if L_prime <= 200 else COEFFICIENTS_GREATER_200
            fitting_params = FITTING_PARAMETERS['flexible'] if self.element_type == "straight flexible" else FITTING_PARAMETERS['smooth']
        
        index = 1 if self.element_type == "straight flexible" else 0
    
        # Calculate the polynomial result
        polynomial_result = ((((((coefficients['6th order'][index] * L_prime + coefficients['5th order'][index]) * L_prime + coefficients['4th order'][index]) * L_prime + coefficients['3rd order'][index]) * L_prime + coefficients['2nd order'][index]) * L_prime + coefficients['1st order'][index]) * L_prime)
    
        # Check for overflow
        if polynomial_result > 1e308:  # This is close to the maximum value for a float in Python
            print("---------------------------------")
            print("Warning: Pressure exceeds 100 mbar. No available pipe diameters for this run.")
            sys.exit(1)  # Exit the program with a status code of 1 indicating an error
            
        P_L_prime = (polynomial_result ** (1 / fitting_params['P2'])) / (self.diameter * 0.001) ** fitting_params['P1']
    
        return P_L_prime

    def get_P_L_prime_plus_L(self, L_prime):
        if self.magnet_type == 1:
            coefficients = COEFFICIENTS_1_5_T
            fitting_params = FITTING_PARAMETERS_1_5_T['flexible'] if self.element_type == "straight flexible" else FITTING_PARAMETERS_1_5_T['smooth']
        else:
            coefficients = COEFFICIENTS_LESS_EQUAL_200 if self.length + L_prime <= 200 else COEFFICIENTS_GREATER_200
            fitting_params = FITTING_PARAMETERS['flexible'] if self.element_type == "straight flexible" else FITTING_PARAMETERS['smooth']
        
        index = 1 if self.element_type == "straight flexible" else 0

        P_L_prime_plus_L = ((((((coefficients['6th order'][index] * (L_prime + self.length) + coefficients['5th order'][index]) * (L_prime + self.length) + coefficients['4th order'][index]) * (L_prime + self.length) + coefficients['3rd order'][index]) * (L_prime + self.length) + coefficients['2nd order'][index]) * (L_prime + self.length) + coefficients['1st order'][index]) * (L_prime + self.length)) ** (1 / fitting_params['P2']) / ((self.diameter * 0.001) ** fitting_params['P1'])

        return P_L_prime_plus_L
    
    def __str__(self):
        return f"Element(diameter={self.diameter}, length={self.length}, angle={self.angle}, type={self.element_type}, magnet={self.magnet_type})"
    

    