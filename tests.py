#!/usr/bin/env python
"""
Unit tests for the pyqcy package.
"""
import unittest
from pyqcy import *

import random


@arbitrary(str)
def str_with_len_lt5():
	length = random.randint(0, 5)
	return ''.join(chr(random.randint(0, 255))
				   for _ in xrange(length))

@qc(s=str_with_len_lt5)
def case_transform_preserves_length(s):
	assert len(s) == len(s.upper())
	assert len(s) == len(s.lower())


class Basic(unittest.TestCase):
	"""Basic test cases.
	"""
	def test_custom_arbitrary(self):
		case_transform_preserves_length.test()


if __name__ == '__main__':
	unittest.main()