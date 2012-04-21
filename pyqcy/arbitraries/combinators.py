"""
Combinators for generators of arbitrary values.
"""
import functools
import collections
import random

from pyqcy.utils import recursive
from pyqcy.arbitraries import is_arbitrary, to_arbitrary


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
