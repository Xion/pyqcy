"""
Properties to be tested.
Also known as "tests".
"""
import inspect
import functools
import sys

from pyqcy.arbitraries import arbitrary, is_arbitrary, to_arbitrary
from pyqcy.results import TestResult
from pyqcy.statistics import Tag
from pyqcy.utils import optional_args


__all__ = ['qc']


@optional_args
class qc(object):
    """Decorator for Python functions that define properties
    to be tested by pyqcy.

    It is expected that default values for function arguments
    define generators that will be used to generate data
    for test cases. See the section about
    :doc:`using generators <arbitraries>` for more information.

    Example of using ``@qc`` to define a test property::

        @qc
        def len_behaves_correctly(
            l=list_(int, min_length=1, max_length=64)
        ):
            assert len(l) == l.__len__()

    """
    def __init__(self, tests=None):
        self.tests_count = tests

    def __call__(self, func):
        """Applies the @qc decorator to given function,
        turning it into a testable property.
        """
        func_args, _, _, func_defaults = inspect.getargspec(func)
        func_args, func_defaults = func_args or [], func_defaults or []
        free_args_count = len(func_args) - len(func_defaults)
        if free_args_count > 0:
            raise TypeError("property has unbound variables: %s" %
                func_args[:free_args_count])
        return Property(func=func,
                        data=dict(zip(func_args, func_defaults)),
                        tests_count=self.tests_count)


class Property(object):
    """A property that can be QuickChecked."""
    tests_count = 100   # used if not overridden on per-property basis

    def __init__(self, func, data, tests_count=None):
        """Constructor. Callers should specify the function
        which encodes the testing property, and arbitrary values'
        generator for test data (function arguments).
        """
        self.func = self.__coerce_to_generator_func(func)
        self.data = dict((k, to_arbitrary(v) if is_arbitrary(v) else v)
                           for k, v in data.iteritems())
        if tests_count is not None:
            self.tests_count = tests_count

    def __coerce_to_generator_func(self, func):
        """Ensures that given function is a generator function,
        i.e. a function that returns a generator.
        This way all properties can be checked in the same manner,
        regardless of whether they use `yield` internally or not.
        """
        if inspect.isgeneratorfunction(func):
            return func

        @functools.wraps(func)
        def generator_func(*args, **kwargs):
            func(*args, **kwargs)
            yield
        return generator_func

    def check(self, count=None):
        """Executes given number of tests for this property
        and gathers statistics about all test runs.

        :param count: Number of tests to execute.
                      If omitted, the default number of tests
                      for this property is executed.

        Returns a list containing a set of "tags"
        for each test case that was executed.
        """
        if count is None:
            count = self.tests_count
        if not (count > 0):
            raise ValueError("test count must be positive")
        return [self.test_one() for _ in xrange(count)]

    def test(self, count=None):
        """Executes given number of tests for this property
        and checks whether they all pass. This is a simplified
        version of :meth:`check` method which discards
        any statistics generated during test runs.

        :param count: Number of tests to execute.
                      If omitted, the default number of tests
                      for this property is executed.

        Returns True if all tests passed. Otherwise,
        re-raises the exception which caused a test to fail.
        """
        results = self.check(count)
        failure = next((r for r in results if not r.succeeded), None)
        if failure:
            failure.propagate_failure()
        return True

    def test_one(self):
        """Executes a single test for this property."""
        data = self.__generate_data()
        result = TestResult(data)
        try:
            coroutine = self.func(**data)
            result.tags = self.__execute_test(coroutine)
        except:
            result.register_failure()

        return result

    def __generate_data(self):
        """Returns a dictionary of test data
        to be passed as keyword arguments to property function.
        """
        return dict((k, next(v) if is_arbitrary(v) else v)
                    for k, v in self.data.iteritems())

    def __execute_test(self, coroutine):
        """Executes given test coroutine and returns
        a set of "tags" that have been assigned to
        the test case by the property.
        """
        res = []
        try:
            while True:
                obj = next(coroutine)
                if obj is not None:
                    value = obj.value if isinstance(obj, Tag) else obj
                    res.append(value)
        except StopIteration:
            return frozenset(res)

    @property
    def parametrized(self):
        '''Checks whether the property is parametrized, i.e. has
        some arguments which are not generators of arbitrary values.
        '''
        return not all(map(is_arbitrary, self.data.itervalues()))

    def __call__(self, **kwargs):
        """Calling the property object will create new one
        with some of the arguments ("variables") bound to given values.
        In other words, it will perform currying on property's function.
        """
        @functools.wraps(self.func)
        def curried_func(**kwargs_):
            final_kwargs = kwargs.copy()
            final_kwargs.update(kwargs_)
            return self.func(**final_kwargs)

        data = dict((k, v) for (k, v) in self.data.iteritems()
                    if k not in kwargs)
        return Property(curried_func, data, self.tests_count)
