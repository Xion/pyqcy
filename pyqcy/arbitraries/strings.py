"""
Generators of arbitrary strings.
"""
import random

from pyqcy.arbitraries import arbitrary, is_arbitrary
from pyqcy.arbitraries.standard import int_


@arbitrary(str)
def str_(of=int_(min=0, max=255), min_length=1, max_length=64):
    """Generator for arbitrary strings.

    Parameters for this generator allow for adjusting the length
    of resulting strings and the set of characters they are composed of.

    :param of: Characters used to construct the strings.
               This can be either an iterable of characters
               (e.g. a string) or a generator that produces them.
    :param min_length: A minimum length of string to generate
    :param max_length: A maximum length of string to generate
    """
    length = random.randint(min_length, max_length)
    char = lambda ch: ch if isinstance(ch, basestring) else chr(ch)
    if is_arbitrary(of):
        return ''.join(char(next(of)) for _ in xrange(length))
    return ''.join(char(random.choice(of)) for _ in xrange(length))
