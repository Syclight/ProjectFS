PI = 3.141592653589793
PI_HALF = 1.5707963267948966
PI_QUARTER = 0.78539816339745
PI_DOUBLE = 6.283185307179586
E = 2.718281828459045


def __f_interpolation_poly__(x):
    return -0.0001521 * x * x * x * x * x * x \
           - 0.003130 * x * x * x * x * x \
           + 0.07321 * x * x * x * x \
           - 0.3577 * x * x * x \
           + 0.2255 * x * x \
           + 0.9038 * x


def __f_interpolation_spline__(x):
    pass
