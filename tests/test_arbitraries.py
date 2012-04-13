"""
Unit tests for arbitraries.
"""
import unittest
from pyqcy import *

import random


class Arbitraries(unittest.TestCase):
    """Test cases for different types of @arbitrary generators."""

    def test_standard_arbitrary(self):
        addition_doesnt_break.test()

    def test_generator_arbitrary(self):
        multiplication_on_floats.test()

    def test_standard_arbitrary_with_args(self):
        addition_works_for_positive_floats.test()

    def test_standard_nested_arbitrary(self):
        sort_finds_minimum.test()

    def test_tuple_arbitrary(self):
        tuples_survive_listification.test()

    def test_shorthand_tuple_arbitrary(self):
        two_is_two.test()

    def test_dict_arbitrary(self):
        dict_update_works.test()

    def test_elements_arbitrary(self):
        set_of_elements.test()

    def test_one_of_arbitrary(self):
        one_of_works.test()

    def test_frequency_arbitrary(self):
        frequency_works.test()

    def test_custom_arbitrary(self):
        case_transform_preserves_length.test()


# Arbitraries

@arbitrary(str)
def str_with_len_lt5():
    length = random.randint(0, 4)
    return ''.join(chr(random.randint(0, 255))
                   for _ in xrange(length))

@arbitrary(float)
def random_floats():
    while True:
        yield random.random()

# Test properties

@qc(int, int)
def addition_doesnt_break(x, y):
    _ = x + y

@qc(float_(min=0.0), float_(min=0.0))
def addition_works_for_positive_floats(x, y):
    sum = x + y
    assert sum >= x and sum >= y

@qc(s=str_with_len_lt5)
def case_transform_preserves_length(s):
    assert len(s) == len(s.upper())
    assert len(s) == len(s.lower())

@qc
def multiplication_on_floats(
    a=random_floats, b=random_floats
):
    assert a * b <= 1.0

@qc
def sort_finds_minimum(
    l=list_(of=int, min_length=1, max_length=64)
):
    assert sorted(l)[0] == min(l)

@qc
def dict_update_works(
    d1=dict_(keys=str, values=str, min_length=1, max_length=64),
    d2=dict_(items=tuple_(int, str), min_length=1, max_length=64)
):
    d1_len = len(d1)
    d1.update(d2)
    assert len(d1) == d1_len + len(d2)

@qc
def tuples_survive_listification(
    t=tuple_(int, n=10)
):
    as_list = list(t)
    back_as_tuple = tuple(as_list)
    assert all((old, new) for (old, new) in zip(t, back_as_tuple))

@qc
def two_is_two(
    t=two(int)
):
    assert len(t) == 2

@qc
def set_of_elements(
    x=elements("abc")
):
    assert len(x) == 1
    assert x in "abc"

@qc
def one_of_works(
    x=one_of(float, int)
):
    assert isinstance(x, (float, int))

@qc
def frequency_works(
    x=frequency([(1, float), (2, int)])
):
    assert isinstance(x, (float, int))
