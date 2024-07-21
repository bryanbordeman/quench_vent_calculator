from calculator.core import PressureCalculator
from calculator.elements import Element
from calculator.constants import MAX_PRESSURE, AVAILABLE_DIAMETERS_MM
from calculator.utils import inch_to_mm, mm_to_inch, inch_to_m, m_to_inch

import itertools

def find_optimal_diameters():
	calc = PressureCalculator()
	optimal_diameters_info = []  # This will store tuples of (diameter_mm, element_type)
	optimal_pressure_drop = float('inf')
	optimal_pressure = 0

	# Define available diameters for each element position
	available_diameters = [
		[inch_to_mm(6)],  # Element[0] fixed at 6 inches
		AVAILABLE_DIAMETERS_MM,  # Element[1] can vary
		AVAILABLE_DIAMETERS_MM,  # Element[2] can vary
		AVAILABLE_DIAMETERS_MM  # Element[3] can vary
	]

	# Iterate over each combination of diameters
	for diameters in itertools.product(*available_diameters):
		# Check if any subsequent diameter is smaller than the previous one
		if any(diameters[i] > diameters[i + 1] for i in range(len(diameters) - 1)):
			continue  # Skip this combination

		elements = [
			Element(diameter=diameters[0], length=0.37, element_type="straight flexible"),
			Element(diameter=diameters[1], length=20.0, element_type="straight smooth"),
			Element(diameter=diameters[2], angle=45, type="smooth", element_type="90° smooth"),
			Element(diameter=diameters[3], length=10.0, element_type="straight smooth"),
		]

		results = calc.calculate_pressure(elements)
		total_pressure = results[-1]['pressure_drop_n']

		# Check if this combination's pressure drop is closer to the MAX_PRESSURE without exceeding it
		if 0 <= MAX_PRESSURE - total_pressure < optimal_pressure_drop:
			optimal_pressure_drop = MAX_PRESSURE - total_pressure
			optimal_diameters_info = [(diameter, element.element_type, element.length) for diameter, element in zip(diameters, elements)]
			optimal_pressure = total_pressure

	return optimal_diameters_info, optimal_pressure


if __name__ == "__main__":
    optimal_diameters_info, optimal_pressure = find_optimal_diameters()
    if optimal_diameters_info:
        print("Optimal Diameters and Types:")
        for diameter_mm, element_type, length in optimal_diameters_info:
            diameter_inch = mm_to_inch(diameter_mm)
            # Check if the first word in element_type is "straight"
            length_display = f"- {m_to_inch(length)} inches ({length} m)" if element_type.split()[0] == "straight" else ""
            print(f"{diameter_inch} inch ({diameter_mm} mm) - {element_type} {length_display}")    
        print(f"Resulting in a total pressure drop of {round(optimal_pressure, 1)} mbar")