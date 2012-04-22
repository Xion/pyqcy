"""
Statistics for test cases.
"""
import collections


__all__ = ['collect', 'classify']


class Tag(object):
    """A tag that can be assigned to a test case.
    It can be any hashable value, i.e. a one that
    could be part of a set, or a key in dictionary.

    This is mostly a marker class - a wrapper that
    is used to distinguish results of statistic function
    calls from other values that could be yielded
    from property function.
    """
    def __init__(self, value):
        if not isinstance(value, collections.Hashable):
            raise TypeError("tag value must be hashable")
        self.value = value


def collect(value):
    """Collects test cases that share the same value
    (passed as argument) for statistical purposes.
    The value can be any hashable.
    Typical usage is as follows:

        @qc
        def sort_works(
            l=list_(int, min_length=1, max_length=64)
        ):
            yield collect(len(l))
            assert list(sorted(l))[0] = min(l)
    """
    return Tag(value)


def classify(condition, label):
    """Classifies test cases depending on whether they satisfy
    given condition. If a test case meets the condition, it will
    "stamped" with given label that will subsequently appear
    in statistical report.
    Typical usage is as follows:

        @qc
        def sort_preserves_length(l=list_(int, max_length=64)):
            yield classify(len(l) == 0, "empty list")
            yield classify(len(l) < 10, "short list")
            assert len(list(sorted(l))) == len(l)
    """
    return Tag(label) if condition else None
