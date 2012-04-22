"""
Unit tests for integration facilities.
"""
import unittest
from pyqcy import *

import os


class Integration(unittest.TestCase):
    """Test cases for the pyqcy test case. (Yes.)"""

    def test_testcase(self):
        """The test case for TestCase."""
        class Sorting(TestCase):
            @qc
            def sort_preserves_length(l=list_(of=int, max_length=128)):
                assert len(l) == len(list(sorted(l)))

            @qc
            def sort_finds_minimum(
                l=list_(of=int, min_length=1, max_length=128)
            ):
                assert min(l) == list(sorted(l))[0]

        suite = unittest.TestLoader().loadTestsFromTestCase(Sorting)
        results = unittest.TextTestRunner(
            stream=open(os.devnull, 'w'),  # we don't want output here
            verbosity=0).run(suite)

        assert results.wasSuccessful()
