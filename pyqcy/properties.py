"""
Properties to be tested.
Also known as "tests".
"""
import inspect
import functools

from .arbitraries import arbitrary, is_arbitrary, to_arbitrary
from .statistics import Tag


__all__ = ['qc']


DEFAULT_TEST_COUNT = 100


class Property(object):
    """A property that can be QuickChecked."""

    def __init__(self, args, kwargs, func):
        """Constructor. Callers should specify the function
        which encodes the testing property, and arbitrary values'
        generator for both positonal and keyword arguments.
        """
        self.args = [to_arbitrary(arg) if is_arbitrary(arg) else arg
                     for arg in args]
        self.kwargs = dict((k, to_arbitrary(v) if is_arbitrary else v)
                           for k, v in kwargs.iteritems())
        self.func = self.__coerce_to_generator_func(func)

    def __coerce_to_generator_func(self, func):
        """Ensures that given function is a generator function,
        i.e. a function that returns a generator.
        This way all properties can be tested the same way,
        regardless of whether they use `yield` internally or not.
        """
        if inspect.isgeneratorfunction(func):
            return func

        @functools.wraps(func)
        def generator_func(*args, **kwargs):
            func(*args, **kwargs)
            yield
        return generator_func

    def test(self, count=DEFAULT_TEST_COUNT):
        """Executes given number of tests for this property
        and gathers statistics about all test runs.
        Returns a list containing a set of "tags"
        for each test case that was executed.
        """
        if not (count > 0):
            raise ValueError("test count must be positive")
        return [self.test_one() for _ in xrange(count)]

    def test_one(self):
        """Executes a single test for this property."""
        args = self.__arbitrary_args()
        kwargs = self.__arbitrary_kwargs()
        coroutine = self.func(*args, **kwargs)
        return self.__execute_test(coroutine)

    def __arbitrary_args(self):
        """Returns a list of arbitrary values for
        positional arguments of the property function.
        """
        return [next(arg) if is_arbitrary(arg) else arg
                for arg in self.args]

    def __arbitrary_kwargs(self):
        """Returns a dictionary of arbitrary values
        for keyword arguments of the property function.
        """
        return dict((k, next(v) if is_arbitrary(v) else v)
                    for k, v in self.kwargs.iteritems())

    def __execute_test(self, coroutine):
        """Executes given test coroutine and returns results.
        The results is a set of "tags" that have been assigned to
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
        args_are_arbitrary = all(map(is_arbitrary, self.args))
        kwargs_are_arbitrary = all(map(is_arbitrary, self.kwargs.itervalues()))
        return not (args_are_arbitrary and kwargs_are_arbitrary)

    def __call__(self, *args, **kwargs):
        """Calling the property object will create new one
        with some of the arguments bound to given values.
        In other words, it will perform currying on property's
        function.
        """
        @functools.wraps(self.func)
        def curried_func(*args_, **kwargs_):
            final_args = list(args) + list(args_ or [])
            final_kwargs = kwargs.copy()
            final_kwargs.update(kwargs_)
            return self.func(*final_args, **final_kwargs)

        curried_args = self.args[len(args):]
        curried_kwargs = dict((k, v) for (k, v) in self.kwargs.iteritems()
                               if k not in kwargs)
        return Property(curried_args, curried_kwargs, curried_func)


# The @qc decorator

class PropertyDecorator(object):
    """Class used to implement the @qc decorator
    which is to be applied on properties.
    """
    def __init__(self, *args, **kwargs):
        self.prop_args = args
        self.prop_kwargs = kwargs

    def __call__(self, func):
        return Property(self.prop_args, self.prop_kwargs, func)


def qc(first_arg=None, *args, **kwargs):
    """@qc decorator to be applied on functions that encode
    QuickCheck properties to be tested.
    """
    # applying @qc on function whose default arguments
    # specify generators of arbitrary values for those arguments
    parameterless_application = (
        inspect.isfunction(first_arg) and
        not is_arbitrary(first_arg) and
        not (args or kwargs)
    )
    if parameterless_application:
        func_args, _, _, func_defaults = inspect.getargspec(first_arg)
        func_args, func_defaults = func_args or [], func_defaults or []
        free_args_count = len(func_args) - len(func_defaults)
        if free_args_count > 0:
            raise TypeError("property has unbound variables: %s" %
                func_args[:free_args_count])
        return Property(args=func_defaults, kwargs={}, func=first_arg)

    # typical application, e.g.: @qc(x=int_, y=float_)
    if first_arg is not None:
        args = [first_arg] + list(args)
    return PropertyDecorator(*args, **kwargs)
