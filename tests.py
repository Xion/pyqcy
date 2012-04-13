#!/usr/bin/env python
"""
Unit tests for the pyqcy package.
"""
import unittest
from pyqcy import *

import random


@arbitrary(str)
def str_with_len_lt5():
    length = random.randint(0, 4)
    return ''.join(chr(random.randint(0, 255))
                   for _ in xrange(length))

@arbitrary(int)
def two_digit_integers():
    return random.randint(10, 99)

@arbitrary(float)
def random_floats():
    while True:
        yield random.random()



@qc(int, int)
def addition_doesnt_break(x, y):
    _ = x + y

@qc(two_digit_integers, two_digit_integers)
def addition_works_within_hundred(x, y):
    assert 20 <= x + y < 200

@qc(float_(min=0.0), float_(min=0.0))
def addition_works_for_positive_floats(x, y):
    sum = x + y
    assert sum >= x and sum >= y

@qc
def subtraction_doesnt_break(x=int, y=int):
    _ = x + y

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


@qc
def failing():
    assert False

@qc
def adding_to(x=0, y=int_(min=0, max=10)):
    assert x + y >= x



class Basic(unittest.TestCase):
    """Basic test cases.
    """
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

    def test_positional_qc_arguments(self):
        addition_works_within_hundred.test()

    def test_arbitraries_in_default_args(self):
        subtraction_doesnt_break.test()

    def test_failing_property(self):
        self.assertRaises(AssertionError, failing.test)

    def test_parametrized_property(self):
        assert adding_to(5).test()

    def test_runner(self):
        from pyqcy.properties import Property
        assert main(exit=False) == len([obj for obj in globals().itervalues()
                                        if isinstance(obj, Property)])


class Statistics(unittest.TestCase):
    """Test cases for statistics functionality."""

    @qc
    def sorting_short_lists(
        l=list_(float, min_length=1, max_length=6)
    ):
        yield collect(len(l))
        assert list(sorted(l))[-1] == max(l)

    @qc
    def sort_preserves_length(l=list_(int, max_length=64)):
        yield classify(len(l) == 0, "empty list")
        yield classify(len(l) % 2 == 0, "even list")
        yield classify(len(l) % 2 != 0, "odd list")
        assert len(list(sorted(l))) == len(l)

    def test_collect(self):
        results = sorting_short_lists.test()
        assert all(len(r) > 0 for r in results)

    def test_classify(self):
        results = sort_preserves_length.test()
        assert any(len(r) > 0 for r in results)



if __name__ == '__main__':
    unittest.main()