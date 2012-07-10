"""
Arbitrary values generators for Python numeric types.
"""
import sys
import random

from pyqcy.arbitraries import arbitrary


@arbitrary(int)
def int_(min=-sys.maxint - 1, max=sys.maxint):
    """Generator for arbitrary integers.

    By default, it generates values from the whole integer range
    supported by operating system; this can be adjusted using
    parameters.

    :param min: A minimum value of integer to generate
    :param max: A maximum value of integer to generate
    """
    return random.randint(min, max)


@arbitrary(float)
def float_(min=-float(sys.maxint), max=float(sys.maxint)):
    """Generator for arbitrary floats.

    :param min: A minimum value of float to generate
    :param max: A maximum value of float to generate
    """
    return min + random.random() * (max - min)


@arbitrary(complex)
def complex_(min_real=-float(sys.maxint), max_real=float(sys.maxint),
             min_imag=-float(sys.maxint), max_imag=float(sys.maxint)):
    """Generator for arbitrary complex numbers
    of the built-in Python complex type.

    Parameters for this generator allow for adjusting the rectangle
    on the complex plane where the values will come from.

    :param min_real: A minimum value for real part of generated numbers
    :param max_real: A maximum value for real part of generated numbers
    :param min_imag: A minimum value for the imaginary part
                     of generated numbers
    :param max_imag: A maximum value for the imaginary part
                     of generated numbers
    """
    reals = float_(min_real, max_real)
    imags = float_(min_imag, max_imag)
    return complex(next(reals), next(imags))
