"""
Unit tests for the pyqcy test runner.
"""
import sys

import unittest
from mocktest import MockTransaction, when, expect

from pyqcy import qc, int_, list_, collect, main


@qc
def addition_success(
    x=int_(min=0), y=int_(min=0)
):
    the_sum = x + y
    assert the_sum >= x and the_sum >= y


@qc
def addition_fail(
    x=int_(min=0), y=int_(min=0)
):
    the_sum = x + y
    assert the_sum >= x and the_sum < y


@qc
def statistics_work(
    l=list_(int, min_length=1, max_length=100)
):
    yield collect(len(l))
    assert list(sorted(l))[0] == min(l)


class Runner(unittest.TestCase):
    """Test cases for the pyqcy test runner (pyqcy.main)."""

    def test_runner(self):
        from pyqcy.properties import Property

        with MockTransaction:
            when(sys).exit.then_return(None)
            assert main(__name__, exit=True) == len([
                obj for obj in globals().itervalues()
                if isinstance(obj, Property)
            ])

            # we have one failing property so expect a failure
            expect(sys).exit.where(lambda code: code != 0).once()
