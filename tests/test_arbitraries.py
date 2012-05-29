"""
Unit tests for arbitraries.
"""
import unittest

import random
import json
import string

from pyqcy import *


class General(unittest.TestCase):
    """General test cases for generators of arbitrary values."""

    def test_standard_arbitrary(self):
        @qc
        def addition_doesnt_break(x=int, y=int):
            _ = x + y

        addition_doesnt_break.test()

    def test_generator_arbitrary(self):
        @arbitrary(float)
        def random_floats():
            while True:
                yield random.random()
        @qc
        def multiplication_on_floats(
            a=random_floats, b=random_floats
        ):
            assert a * b <= 1.0

        multiplication_on_floats.test()

    def test_standard_arbitrary_with_args(self):
        @qc
        def addition_works_for_positive_floats(
            x=float_(min=0.0), y=float_(min=0.0)
        ):
            sum = x + y
            assert sum >= x and sum >= y

        addition_works_for_positive_floats.test()

    def test_custom_arbitrary(self):
        @arbitrary(str)
        def str_with_len_lt5():
            length = random.randint(0, 4)
            return ''.join(chr(random.randint(0, 255))
                           for _ in xrange(length))
        @qc
        def case_transform_preserves_length(
            s=str_with_len_lt5
        ):
            assert len(s) == len(s.upper())
            assert len(s) == len(s.lower())

        case_transform_preserves_length.test()

    def test_standard_nested_arbitrary(self):
        @qc
        def sort_finds_minimum(
            l=list_(of=int, min_length=1, max_length=64)
        ):
            assert sorted(l)[0] == min(l)

        sort_finds_minimum.test()


class Strings(unittest.TestCase):
    """Test cases for arbitrary generators producing strings."""

    def test_unicode_arbitrary(self):
        @qc
        def case_transform_on_unicode(
            s=unicode_(min_length=2, max_length=128)
        ):
            assert s.upper() == s.upper().upper()

        case_transform_on_unicode.test()

    def test_regex_arbitrary(self):
        @qc
        def pattern_is_a_pattern(s=regex(r'\d+')):
            assert len(s) > 0
            assert all(c in string.digits for c in s)
        @qc
        def email_is_email(s=email()):
            assert '@' in s
            assert s.rfind('.') > s.find('@') # at least one dot after @

        pattern_is_a_pattern.test()
        email_is_email.test()

    def test_ipv4(self):
        @qc
        def ipv4_is_within_range(ip=ipv4()):
            assert all(0 <= int(part) <= 255 for part in ip.split('.'))

        ipv4_is_within_range.test()


class Collections(unittest.TestCase):
    """Test cases for generators producing arbitrary collections."""

    def test_tuple_arbitrary(self):
        @qc
        def tuples_survive_listification(t=tuple_(int, n=10)):
            as_list = list(t)
            back_as_tuple = tuple(as_list)
            assert all((old, new) for (old, new) in zip(t, back_as_tuple))

        tuples_survive_listification.test()

    def test_shorthand_tuple_arbitrary(self):
        @qc
        def two_is_two(t=two(int)):
            assert len(t) == 2

        two_is_two.test()

    def test_dict_arbitrary(self):
        @qc
        def dict_update_works(
            d1=dict_(keys=str, values=str, min_length=1, max_length=64),
            d2=dict_(items=tuple_(int, str), min_length=1, max_length=64)
        ):
            d1_len = len(d1)
            d1.update(d2)
            assert len(d1) == d1_len + len(d2)

        dict_update_works.test()


class Combinators(unittest.TestCase):
    """Test cases for arbitrary combinators.."""

    def test_apply(self):
        @qc
        def apply_works_with_functions(
            x=apply(json.dumps,
                    list_(of=int, min_length=1, max_length=64))
        ):
            assert isinstance(x, basestring)
            assert all(isinstance(i, int) for i in json.loads(x))

        @qc
        def apply_works_with_types(x=apply(str, int)):
            assert isinstance(x, str)

        apply_works_with_functions.test()
        apply_works_with_types.test()

    def test_data(self):
        @qc
        def data_works_with_lists(
            x=data([int, str])
        ):
            assert isinstance(x, list)
            assert len(x) == 2
            assert isinstance(x[0], int) and isinstance(x[1], str)

        @qc
        def data_works_with_tuples(
            x=data((float, str, int))
        ):
            assert isinstance(x, tuple)
            assert len(x) == 3
            for i, t in enumerate((float, str, int)):
                assert isinstance(x[i], t)

        @qc
        def data_works_with_dictionaries(x=data({
            'login': str_(of='abcdefghijklmnopqrstuvwxyz',
                          min_length=4, max_length=16),
            'password': str_(min_length=8, max_length=64),
        })):
            assert isinstance(x, dict)
            assert len(x) == 2
            assert 'login' in x and 'password' in x
            assert isinstance(x['login'], str) and isinstance(x['password'], str)

        data_works_with_lists.test()
        data_works_with_tuples.test()
        data_works_with_dictionaries.test()

    def test_elements_arbitrary(self):
        @qc
        def set_of_elements(x=elements("abc")):
            assert len(x) == 1
            assert x in "abc"

        set_of_elements.test()

    def test_one_of_arbitrary(self):
        @qc
        def one_of_works(x=one_of(float, int)):
            assert isinstance(x, (float, int))

        one_of_works.test()

    def test_frequency_arbitrary(self):
        @qc
        def frequency_works(x=frequency([(1, float), (2, int)])):
            assert isinstance(x, (float, int))

        frequency_works.test()
