"""
Statistics for test cases.
"""
import collections


__all__ = ['collect', 'classify']


class Tag(object):
    """A tag that can be assigned to a test case.

    It can be any hashable value, i.e. a one that
    could be a set element or dictionary key.

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

    :param value: Value to collect. This can be any hashable,
                  i.e. a value that could be a set element
                  or dictionary key.

    Typical usage of `collect` is as follows:

    .. code-block:: python

        @qc
        def sort_works(
            l=list_(int, min_length=1, max_length=100)
        ):
            yield collect(len(l))
            assert list(sorted(l))[0] = min(l)

    Checking the above property will produce output similar to this:

    .. code-block:: console

        sort_works: passed 100 tests.
        1.00%: 1
        1.00%: 2
        ...
        1.00%: 100
    """
    return Tag(value)


def classify(condition, label):
    """Classifies test cases depending on whether they satisfy
    given condition.

    If a test case meets the condition, it will be "stamped"
    with given label that will subsequently appear in statistical report
    displayed after a property has been tested.

    :param condition: Condition that the test data should satisfy
                      in order for the test case to be stamped with `label`.
    :param label: A label to be associated with this test case
                  if `condition` turns out to be true

    Typical usage is as follows:

    .. code-block:: python

        @qc
        def sort_preserves_length(
            l=list_(int, min_length=1, max_length=100)
        ):
            yield classify(len(l) == 0, "empty list")
            yield classify(len(l) < 10, "short list")
            assert len(list(sorted(l))) == len(l)

    Checking the above property will produce
    something like the following output:

    .. code-block::  console

        sort_preserves_length: passed 100 tests.
        1.00%: empty list, short list
        9.00%: short list
        90.00%: <rest>
    """
    satisfied = condition() if callable(condition) else bool(condition)
    return Tag(label) if satisfied else None
