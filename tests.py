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


class Basic(unittest.TestCase):
	"""Basic test cases.
	"""
	def test_standard_arbitrary(self):
		addition_doesnt_break.test()

	def test_standard_arbitrary_with_args(self):
		addition_works_for_positive_floats.test()

	def test_standard_nested_arbitrary(self):
		sort_finds_minimum.test()

	def test_dict_arbitrary(self):
		dict_update_works.test()

	def test_custom_arbitrary(self):
		case_transform_preserves_length.test()

	def test_positional_qc_arguments(self):
		addition_works_within_hundred.test()

	def test_arbitraries_in_default_args(self):
		subtraction_doesnt_break.test()

	def test_runner(self):
		from pyqcy.properties import Property
		assert main() == len([obj for obj in globals().itervalues()
							  if isinstance(obj, Property)])


if __name__ == '__main__':
	unittest.main()