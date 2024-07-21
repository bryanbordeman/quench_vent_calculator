from calculator.constants import MAX_PRESSURE, AVAILABLE_DIAMETERS_MM

class PressureCalculator:
    def __init__(self):
        self.max_pressure = MAX_PRESSURE
    
    def calculate_pressure(self, elements):
        if not elements:  # Check if elements list is empty
            return []  # Return an empty list or raise an error as appropriate
        
        total_pressure = 0
        results = []
        length_so_far = 0
        n = 1  # Initialize n
        
        for i, element in enumerate(elements):
            if element.diameter not in AVAILABLE_DIAMETERS_MM:
                raise ValueError(f"Diameter {element.diameter} is not available. Choose from {AVAILABLE_DIAMETERS_MM}.")
            
            prev_pressure_drop = results[i-1]['pressure_drop_n'] if i > 0 else 0
            
            pressure_drop_contribution = element.calculate_pressure(prev_pressure_drop, length_so_far, n)
            length_so_far += element.length  # Assuming all elements have a length attribute
            total_pressure += pressure_drop_contribution
            n += 1  # Increment n for each segment
            
            result = {
                'element_type': element.element_type,
                'diameter': element.diameter,
                'length': element.length,  # Simplified to 'length'
                'pressure_drop_n-1': prev_pressure_drop,
                'pressure_drop_n': total_pressure,  # Ensure this key is correctly set
                'pressure_drop_contribution': pressure_drop_contribution,
            }
            results.append(result)
        
        return results