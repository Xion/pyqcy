"""
Unit tests for integration facilities.
"""
import unittest
from pyqcy import *

import os


class Integration(unittest.TestCase):
    """Test cases for the pyqcy test case. (Yes.)"""
    class Sorting(TestCase):
        @qc(tests=1)
        def sort_preserves_length(l=list_(of=int, max_length=128)):
            assert len(l) == len(list(sorted(l)))

        @qc(tests=1)
        def sort_finds_minimum(
            l=list_(of=int, min_length=1, max_length=128)
        ):
            assert min(l) == list(sorted(l))[0]

    def setUp(self):
        loader = unittest.TestLoader()
        self.qc_suite = loader.loadTestsFromTestCase(Integration.Sorting)

    def test_running_testcase(self):
        results = unittest.TextTestRunner(
            stream=open(os.devnull, 'w'),  # we don't want output here
            verbosity=0).run(self.qc_suite)

        assert results.wasSuccessful()

    def test_property_names_in_test_description(self):
        from pyqcy.properties import Property

        test_descriptions = set(tm._testMethodDoc
                                for tm in self.qc_suite._tests)

        assert all("pyqcy" in td for td in test_descriptions)
        assert all(any(k in td for td in test_descriptions)
                   for (k, v) in Integration.Sorting.__dict__.iteritems()
                   if isinstance(v, Property))
