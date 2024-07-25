from calculator.elements import Element
from find_optimal_diameter import find_optimal_diameters
from calculator.utils import inch_to_mm, mm_to_inch, inch_to_m, m_to_inch

# Predefine the VIBRATION_DECOUPLER elements
vibration_decoupler_3_0_T = [Element(diameter=inch_to_mm(6), length=0.37, element_type="straight flexible", magnet_type=2)]
vibration_decoupler_1_5_T = [
    Element(diameter=inch_to_mm(4), length=0.27, element_type="straight flexible", magnet_type=1), # VIBRATION_DECOUPLER
    Element(diameter=inch_to_mm(4), length=0.135, element_type="straight smooth", magnet_type=1)   # VIBRATION_DECOUPLER
]

def choose_elements():
    elements = []
    print("Choose magnet type:")
    magnet_options = {"1": "1.5T", "2": "3.0T"}
    for option, description in magnet_options.items():
        print(f"{option}. {description}")
    magnet_choice = input("Enter your choice (1 or 2): ")
    while magnet_choice not in magnet_options:
        print("Invalid choice. Please enter '1' for 1.5T or '2' for 3.0T.")
        magnet_choice = input("Choose magnet type (1 or 2): ")
    magnet_type = int(magnet_choice)

    # Add predefined VIBRATION_DECOUPLER elements
    if magnet_type == 1:
        elements = vibration_decoupler_1_5_T.copy()
    else:
        elements = vibration_decoupler_3_0_T.copy()
    
    while True:
        print("\nChoose an element to add:")
        element_options = {
            "1": "Straight flexible",
            "2": "Straight smooth",
            "3": "90° elbow",
            "4": "45° elbow",
            "5": "Done adding elements"
        }
        for option, description in element_options.items():
            print(f"{option}. {description}")
        choice = input("Enter your choice (1-5): ")

        if choice == "1" or choice == "2":
            length = float(input("Enter length in meters: "))
            element_type = "straight flexible" if choice == "1" else "straight smooth"
            elements.append(Element(diameter=0, length=length, element_type=element_type, magnet_type=magnet_type))

        elif choice == "3" or choice == "4":
            angle = 90 if choice == "3" else 45
            print("Choose elbow type:")
            print("1. Segmented")
            print("2. Smooth")
            print("3. Mitred")
            elbow_type_choice = input("Enter your choice (1-3): ")
            elbow_types = {"1": 'segmented', "2": 'smooth', "3": 'mitred'}

            while elbow_type_choice not in elbow_types:
                print("Invalid choice. Please enter '1' for Segmented, '2' for Smooth, or '3' for Mitred.")
                elbow_type_choice = input("Enter your choice (1-3): ")

            elbow_type = elbow_types[elbow_type_choice]
            elements.append(Element(diameter=0, angle=angle, type=elbow_type, element_type=f"{angle}° {elbow_type}", magnet_type=magnet_type))
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    return elements, magnet_type

if __name__ == "__main__":
    elements, magnet_type = choose_elements()
    if elements:
        optimal_diameters_info, optimal_pressure = find_optimal_diameters(elements, magnet_type)
        if optimal_diameters_info:
            print("\nOptimal Diameters:")
            for diameter_mm, element_type, length, angle in optimal_diameters_info:
                diameter_inch = mm_to_inch(diameter_mm)
                if length:
                    length_display = f"- {m_to_inch(round(length,2))} inches ({round(length,2)} m)"
                    print(f"{diameter_inch} inch ({diameter_mm} mm) - {element_type} {length_display}")
                else:
                    print(f"{diameter_inch} inch ({diameter_mm} mm) - {element_type} - {angle}°")
            print(f"Resulting in a total pressure drop of {round(optimal_pressure, 1)} mbar")
    else:
        print("No elements selected.")