from calculator.core import PressureCalculator
from calculator.elements import Element
from calculator.utils import inch_to_mm, mm_to_inch, inch_to_m

def main():
    calc = PressureCalculator()
    
    # Define the elements based on the spreadsheet data
    elements = [
        Element(diameter=inch_to_mm(6), length=0.37, element_type="straight flexible"), #VIBRATION_DECOUPLER
        Element(diameter=inch_to_mm(8), length=10.0, element_type="straight smooth"),
        Element(diameter=inch_to_mm(8), angle=45, type="smooth", element_type="90° smooth"),
        Element(diameter=inch_to_mm(8), length=1.0, element_type="straight flexible"),
    ]
    
    results = calc.calculate_pressure(elements)
    
    total_pressure = results[-1]['pressure_drop_n']
    print(f"Total Pressure Drop: {round(total_pressure,1)} mbar")
    
    if total_pressure > 100:
        print("Warning: Pressure exceeds 100 mbar. Consider using a larger diameter pipe.")

if __name__ == "__main__":
    main()