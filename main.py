from calculator.core import PressureCalculator
from calculator.elements import Element
from calculator.utils import inch_to_mm, mm_to_inch, inch_to_m
from choose_elements import choose_elements

def main():
    calc = PressureCalculator()

    # Predefine the VIBRATION_DECOUPLER element
    vibration_decoupler_3_0_T = [Element(diameter=inch_to_mm(6), length=0.37, element_type="straight flexible", magnet_type=2)]
    vibration_decoupler_1_5_T = [
        Element(diameter=inch_to_mm(4), length=0.27, element_type="straight flexible", magnet_type=1), #VIBRATION_DECOUPLER
        Element(diameter=inch_to_mm(4), length=0.135, element_type="straight smooth", magnet_type=1), #VIBRATION_DECOUPLER
    ]
    # Use the choose_elements function to define additional elements based on user input
    # elements = vibration_decoupler + choose_elements()
    # elements = choose_elements()
    
    magnet_type = 1
    # Define the elements based on the spreadsheet data
    elements = []
    if magnet_type == 1:
        elements = vibration_decoupler_1_5_T
    else:
        elements = vibration_decoupler_3_0_T
    
    elements.append(Element(diameter=inch_to_mm(6), length=1, element_type="straight smooth", magnet_type=magnet_type))
    elements.append(Element(diameter=inch_to_mm(6), angle=90, type="smooth", element_type="90° smooth", magnet_type=1),)
    elements.append(Element(diameter=inch_to_mm(6), angle=45, type="smooth", element_type="45° smooth", magnet_type=1),)
    elements.append(Element(diameter=inch_to_mm(6), length=1, element_type="straight flexible", magnet_type=magnet_type))
    elements.append(Element(diameter=inch_to_mm(6), length=2, element_type="straight smooth", magnet_type=magnet_type))
    
    # results = calc.calculate_pressure(elements[0])
    results = calc.calculate_pressure(elements)

    # for i in elements[0]:
    #     print(i)
    
    total_pressure = results[-1]['pressure_drop_n']
    print(f"Total Pressure Drop: {round(total_pressure,1)} mbar")
    
    if total_pressure > 100:
        print("Warning: Pressure exceeds 100 mbar. Consider using a larger diameter pipe.")

if __name__ == "__main__":
    main()