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

@qc(s=str_with_len_lt5)
def case_transform_preserves_length(s):
	assert len(s) == len(s.upper())
	assert len(s) == len(s.lower())



class Basic(unittest.TestCase):
	"""Basic test cases.
	"""
	def test_standard_arbitrary(self):
		addition_doesnt_break.test()

	def test_standard_arbitrary_with_args(self):
		addition_works_for_positive_floats.test()

	def test_custom_arbitrary(self):
		case_transform_preserves_length.test()

	def test_positional_qc_arguments(self):
		addition_works_within_hundred.test()


if __name__ == '__main__':
	unittest.main()