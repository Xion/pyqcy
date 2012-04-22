"""
Combinators for generators of arbitrary values.
"""
import functools
import collections
import inspect
import random

from pyqcy.arbitraries import arbitrary, is_arbitrary, to_arbitrary
from pyqcy.utils import recursive


def apply(func, *args, **kwargs):
    """Creates a generator that applies a function to objects
    returned by given generator(s). Arguments to that function
    will be passed in the same manner as the generators have
    been passed to apply(), i.e. positional args will be passed
    as positional and keyword as keyword.
    """
    if not func:
        raise ValueError("no function provided")
    if not callable(func):
        raise TypeError("expected a callable")

    func_args = [next(to_arbitrary(arg)) for arg in args]
    func_kwargs = dict((k, next(to_arbitrary(v)))
                       for (k, v) in kwargs.iteritems())

    @arbitrary
    def generator():
        return func(*func_args, **func_kwargs)
    return generator


def data(schema):
    """Creates a generator which outputs data structures conforming
    to given schema. Schema can be a list or dictionary that contains
    either immediate values or other arbitrary generators.
    """
    if schema is None:
        raise ValueError("no schema specified")

    is_data_structure = (isinstance(schema, collections.Iterable)
                         and not inspect.isgenerator(schema))
    if not is_data_structure:
        raise TypeError("schema must be a data structure")

    def instance_of(s):
        """Constructs a new data structure instance conforming
        to given schema. This functions proceeds recursively.
        """
        if isinstance(s, collections.Mapping):
            res = {}
            items = s.iteritems()
        else:
            res = [None] * len(s)
            items = enumerate(s)

        for key, value in items:
            if is_arbitrary(value):
                value = to_arbitrary(value)
                res[key] = next(value)
            elif isinstance(value, collections.Iterable):
                res[key] = instance_of(value)
            else:
                res[key] = value
        return res

    @arbitrary
    def generator():
        return instance_of(schema)
    return generator


def combinator(func):
    """Decorator for arbitrary combinator functions which take
    a collection of arguments as either an actual list/sequence,
    or as positional arguments. In other words, it makes
    it possible to use the following two forms of invocation:
    >>> func([1, 2, 3])
    >>> func(1, 2, 3)
    In both cases func() receives 1, 2 and 3 as
    positional arguments (*args).
    """
    _2arbitrary = recursive(lambda obj: to_arbitrary(obj)
                                        if is_arbitrary(obj) else obj)

    @arbitrary
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if not args:
            return func(**kwargs)

        new_args = []
        for arg in args:
            arg_collection = (isinstance(arg, collections.Iterable)
                              and not is_arbitrary(arg))
            if arg_collection:
                arg = map(_2arbitrary, arg)
                new_args.extend(arg)
            else:
                arg = _2arbitrary(arg)
                new_args.append(arg)
        return func(*new_args, **kwargs)

    return wrapped


@combinator
def elements(*args):
    """Creates a generator that returns a random element from those given.
    Every element has equal probability of being picked.
    """
    if not args:
        raise ValueError("cannot pick random element from empty sequence")
    return random.choice(args)


@combinator
def one_of(*args):
    """Creates a generator that chooses among given generators, giving
    equal probability to each one.
    """
    if not args:
        raise ValueError("no generators to choose from")
    return next(random.choice(args))


@combinator
def frequency(*args):
    """Creates a generator that chooses among given generators, according
    to probability (frequency) assigned to them. Function accepts pairs
    (or list of pairs) where the first element is the probability
    and the second element is a particular generator.
    """
    if not args:
        raise ValueError("no generators to choose from")

    freq_sum = sum((p for p, _ in args), 0)
    i = int(random.random() * freq_sum)

    s = 0
    for p, gen in args:
        if s <= i < s + p:
            return next(gen)
        s += p
