"""
Unit tests from properties.
"""
import unittest
from pyqcy import *


class Properties(unittest.TestCase):
    """Test cases for functionality related to properties."""

    def test_positional_qc_arguments(self):
        addition_works_within_hundred.test()

    def test_arbitraries_in_default_args(self):
        subtraction_doesnt_break.test()

    def test_failing_property(self):
        self.assertRaises(AssertionError, failing.test)

    def test_parametrized_property(self):
        assert adding_to(5).test()


# Arbitraries

@arbitrary(int)
def two_digit_integers():
    return random.randint(10, 99)

# Test properties

@qc(two_digit_integers, two_digit_integers)
def addition_works_within_hundred(x, y):
    assert 20 <= x + y < 200

@qc
def subtraction_doesnt_break(x=int, y=int):
    _ = x + y

@qc
def failing():
    assert False

@qc
def adding_to(x=0, y=int_(min=0, max=10)):
    assert x + y >= x