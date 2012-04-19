"""
Integration between pyqcy and other testing libraries,
especially test runners (such as unittest or nose).
"""
import unittest

from .properties import Property
from .runner import run_tests


__all__ = ['TestCase']


class TestCase(unittest.TestCase):
    """Test case containing pyqcy properties that should be tested
    automatically, as part of a standard unit test run.
    Properties should be defined directly within a subclass,
    using a standard @qc decorator - for example:

        class Sorting(TestCase):
            '''Properties that must hold for a sorting.'''
            @qc
            def sort_preserves_length(l=list_(of=int, max_length=128)):
                assert len(l) == len(list(sorted(l)))
            @qc
            def sort_finds_minimum(
                l=list_(of=int, min_length=1, max_length=128)
            ):
                assert min(l) == list(sorted(l))[0]

    Since pyqcy.TestCase is a subclass of standard unittest.TestCase,
    it will be discovered by unittest.main(), nosetests and similar
    testing utilities.
    """
    def test(self):
        """Runs tests for all properties defined within this class."""
        props = [v for v in self.__class__.__dict__.itervalues()
                 if isinstance(v, Property)]
        run_tests(props)
