AVAILABLE_DIAMETERS_INCH = [4, 6, 8, 10, 12, 14, 16]
AVAILABLE_DIAMETERS_MM = [round(d * 25.4, 3) for d in AVAILABLE_DIAMETERS_INCH]

# Updated coefficients
COEFFICIENTS_LESS_EQUAL_200 = {
    '1st order':    [5.39E-02, 2.04E-01,   1.90E+01,   4.80E+00],
    '2nd order':    [5.30E-04, -2.62E-03,  -1.63E+00,  1.87E-01],
    '3rd order':    [-4.53E-06, 2.92E-05,   2.47E-01,   3.86E-02],
    '4th order':    [1.67E-08, -1.99E-07,  -1.62E-02,  -2.10E-03],
    '5th order':    [-2.93E-11, 7.32E-10,   5.32E-04,   6.29E-05],
    '6th order':    [1.96E-14, -1.11E-12,  -6.91E-06,  -6.92E-07],
}

COEFFICIENTS_GREATER_200 = {
    '1st order':	[8.23E-02,   1.30E-01,   1.44E+01,   4.80E+00],
    '2nd order':	[-5.02E-05,  -3.97E-04,  3.17E-02,   1.87E-01],
    '3rd order':    [3.07E-08,   9.26E-07,   8.04E-03,   3.86E-02],
    '4th order':    [-8.91E-12,  -1.28E-09,  -1.69E-04,  -2.10E-03],
    '5th order':    [-3.33E-16,  9.36E-13,   1.65E-06,   6.29E-05],
    '6th order':    [5.16E-19,   -2.80E-16,  -6.05E-09,  -6.92E-07]
}

COEFFICIENTS_1_5_T = { 
    '1st order':	[2.32E-02,  8.09E-02,   4.37E+01,   8.40E+00],
    '2nd order':	[5.09E-05,	-7.42E-04,	-2.24E+00,	9.89E+00],
    '3rd order':	[-6.62E-07,	4.90E-06,	2.00E+00,	-5.27E+00],
    '4th order':	[2.46E-09,	-1.58E-08,	-2.25E-01,	2.31E+00],
    '5th order':	[-3.96E-12,	1.92E-11,	9.30E-03,	-3.98E-01],
    '6th order':	[2.35E-15,	0.00E+00,	0.00E+00,	2.46E-02]
}

TUBE_TYPES = [
    "straight smooth",
    "straight flexible",
    "45° smooth",
    "90° smooth",
    "45° segmented",
    "90° segmented",
    "vibration decoupler",
]

FITTING_PARAMETERS = {
    "smooth": {'P1': 5.2, 'P2': 0.77, 'L1': 5.25, 'L2': 0.74},
    "flexible": {'P1': 5.35, 'P2': 0.63, 'L1': 5.35, 'L2': 0.67}
}

FITTING_PARAMETERS_1_5_T = {
    "smooth": {'P1': 5.2, 'P2': 0.714, 'L1': 5.25, 'L2': 0.68},
    "flexible": {'P1': 5.3, 'P2': 0.65, 'L1': 5.3, 'L2': 0.55}
}

MAX_PRESSURE = 100  # mbar

LENGTH_MULTIPLIERS = {
    "straight smooth": [0.0, 1.0],
    "straight flexible": [0.0, 1.0],
    "45° smooth": [1.0, 0.0],
    "90° smooth": [1.5, 0.0],
    "45° segmented": [1.7, 0.0],
    "90° segmented": [2.5, 0.0],
    "90° mitred": [8.3, 0.0],
}