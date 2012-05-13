"""
Unit tests from properties.
"""
import unittest
from pyqcy import *


CUSTOM_TESTS_COUNT = 134


class Properties(unittest.TestCase):
    """Test cases for functionality related to properties."""

    def test_passing_property(self):
        subtraction_doesnt_break.test()

    def test_failing_property(self):
        self.assertRaises(AssertionError, failing.test)

    def test_parametrized_property(self):
        assert adding_to(5).test()

    def test_number_of_tests_in_decorator(self):
        results = multiplication_works.test()
        assert len(results) == multiplication_works.tests_count
        assert len(results) == CUSTOM_TESTS_COUNT


# Test properties

@qc
def subtraction_doesnt_break(x=int, y=int):
    _ = x - y


@qc
def failing():
    assert False


@qc
def adding_to(x=0, y=int_(min=0, max=10)):
    assert x + y >= x


@qc(tests=CUSTOM_TESTS_COUNT)
def multiplication_works(x=int):
    assert x * 1 == x
