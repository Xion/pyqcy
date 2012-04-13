"""
Unit tests for statistics.
"""
import unittest
from pyqcy import *


class Statistics(unittest.TestCase):
    """Test cases for statistics functionality."""

    def test_collect(self):
        results = sorting_short_lists.test()
        assert all(len(r) > 0 for r in results)

    def test_classify(self):
        results = sort_preserves_length.test()
        assert any(len(r) > 0 for r in results)


# Test properties

@qc
def sorting_short_lists(
    l=list_(float, min_length=1, max_length=6)
):
    yield collect(len(l))
    assert list(sorted(l))[-1] == max(l)

@qc
def sort_preserves_length(l=list_(int, max_length=64)):
    yield classify(len(l) == 0, "empty list")
    yield classify(len(l) % 2 == 0, "even list")
    yield classify(len(l) % 2 != 0, "odd list")
    assert len(list(sorted(l))) == len(l)