"""
Unit tests for the pyqcy test runner.
"""
import unittest
from pyqcy import *


class Runner(unittest.TestCase):
    """Test cases for the pyqcy test runner (pyqcy.main)."""

    def test_runner(self):
        """Tests the runner. This uses all the @qc properties
        from all test modules imported by nosetests, and runs
        them under our test harness to verify it functions
        properly.
        """
        from pyqcy.properties import Property
        assert main(exit=False) == len([obj for obj in globals().itervalues()
                                        if isinstance(obj, Property)])