"""
Integration between pyqcy and other testing libraries,
especially test runners (such as unittest or nose).
"""
import unittest

from .properties import Property
from .runner import run_tests


__all__ = ['TestCase']


class TestCase(unittest.TestCase):
    """`unittest` test case for pyqcy properties.

    Properties defined here within subclasses of :class:`TestCase`
    will be verified automatically as a part of standard `unittest` run.
    To define them, use the typical syntax with :func:`qc` decorator::

        class Sorting(TestCase):
            '''Properties that must hold for a sorting.'''
            @qc
            def sort_preserves_length(
                l=list_(of=int, max_length=128)
            ):
                assert len(l) == len(list(sorted(l)))
            @qc
            def sort_finds_minimum(
                l=list_(of=int, min_length=1, max_length=128)
            ):
                assert min(l) == list(sorted(l))[0]

    Since :class:`TestCase` itself is a subclass of standard
    :class:`unittest.TestCase`, it will be discovered by :func:`unittest.main`,
    `nosetests` or similar testing utilities.
    """
    class __metaclass__(type):
        def __new__(cls, name, bases, dict_):
            """Create ``TestCase`` class that contains properties to check."""
            properties = dict((k, v) for (k, v) in dict_.iteritems()
                              if isinstance(v, Property))

            # include a test() method that runs all property tests
            # and has proper docstring to show when verbose mode is used
            def test(self):
                run_tests(properties.itervalues(), propagate_exc=True)
            test.__doc__ = "[pyqcy] %s" % ", ".join(properties.iterkeys())

            dict_['test'] = test
            return type.__new__(cls, name, bases, dict_)
