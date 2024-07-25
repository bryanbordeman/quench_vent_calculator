from calculator.core import PressureCalculator
from calculator.constants import MAX_PRESSURE, AVAILABLE_DIAMETERS_MM
from calculator.utils import mm_to_inch, inch_to_m, m_to_inch

import itertools

def find_optimal_diameters(elements, magnet_type):
    calc = PressureCalculator()
    optimal_diameters_info = []  # This will store tuples of (diameter_mm, element_type)
    optimal_pressure_drop = float('inf')
    optimal_pressure = 0

    # Determine the number of elements to exclude based on magnet_type 1.5T or 3.0T both are vibration_decoupler elements
    exclude_count = 2 if magnet_type == 1 else 1

    # Adjust available diameters based on the exclude_count
    available_diameters = [element.diameter for element in elements[:exclude_count]] + [AVAILABLE_DIAMETERS_MM] * (len(elements) - exclude_count)

    print(available_diameters)

    for diameters in itertools.product(*available_diameters[exclude_count:]):
        diameters = tuple(element.diameter for element in elements[:exclude_count]) + diameters  # Prepend the static diameters

        if any(diameters[i] > diameters[i + 1] for i in range(len(diameters) - 1)):
            continue  # Skip this combination

        for element, diameter in zip(elements, diameters):
            element.diameter = diameter

        results = calc.calculate_pressure(elements)
        total_pressure = results[-1]['pressure_drop_n']

        if 0 <= MAX_PRESSURE - total_pressure < optimal_pressure_drop:
            optimal_pressure_drop = MAX_PRESSURE - total_pressure
            optimal_diameters_info = [(diameter, element.element_type, getattr(element, 'length', 0), getattr(element, 'angle', 0)) for diameter, element in zip(diameters, elements)]
            optimal_pressure = total_pressure

    return optimal_diameters_info, optimal_pressure