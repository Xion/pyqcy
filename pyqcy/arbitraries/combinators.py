"""
Combinators for generators of arbitrary values.
"""
import functools
import inspect
import random

from collections import Iterable, Mapping
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict # fallback for Python 2.6

from pyqcy.arbitraries import arbitrary, is_arbitrary, to_arbitrary
from pyqcy.utils import recursive


def apply(func, *args, **kwargs):
    """Generator that applies a specific function to objects returned
    by given generator(s).

    Any number of generators can be passed as arguments, and they can
    be both positional (`args`) or keyword arguments (`kwargs`).
    In any case, the same invocation style (i.e. positional or keyword)
    will be used when calling the `func` with actual values
    obtained from generators.

    As an example, the following call::

        apply(json.dumps, dict_(items=two(str)))

    will create a generator that yields results of `json.dumps(d)` invocations,
    where `d` is an arbitrary dictionary that maps strings to strings.

    Similarly, using `apply` as shown below::

        apply(itertools.product, list_(of=int), repeat=4)

    gets us a generator that produces results of
    `itertools.product(l, repeat=4)`, where `l` is an arbitrary list of `int`\ s.
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
    """Generator that outputs data structures conforming to given schema.

    :param schema: A list or dictionary that contains either
                   immediate values or other generators.

    .. note::

       `schema` can be recursive and combine lists with dictionaries
       into complex structures. You can have nested dictionaries,
       lists containing lists, dictionaries with lists as values, and so on.

    A typical example of using `data`:

    .. code-block:: python

        import string

        @qc
        def creating_user_works(
            request=data({
                'login': str_(of=string.ascii_letters | string.digits,
                              min_length=3, max_length=32),
                'password': str_(min_length=8, max_length=128),
            })
        ):
            response = create_user(request['login'], request['password'])
            assert response['status'] == "OK
    """
    if schema is None:
        raise ValueError("no schema specified")

    is_data_structure = (isinstance(schema, Iterable)
                         and not inspect.isgenerator(schema))
    if not is_data_structure:
        raise TypeError("schema must be a data structure")

    def instance_of(s):
        """Constructs a new data structure instance conforming
        to given schema. This function proceeds recursively.
        """
        if isinstance(s, Mapping):
            res = (OrderedDict()
                   if isinstance(s, OrderedDict)
                   else dict())
            items = s.iteritems()
        else:
            res = [None] * len(s)
            items = enumerate(s)

        for key, value in items:
            if is_arbitrary(value):
                value = to_arbitrary(value)
                res[key] = next(value)
            elif isinstance(value, Iterable):
                res[key] = instance_of(value)
            else:
                res[key] = value

        if isinstance(s, tuple):
            res = tuple(res)
        return res

    @arbitrary
    def generator():
        return instance_of(schema)
    return generator


def combinator(func):
    """Decorator for arbitrary combinator functions which take
    a collection of arguments as either an actual list/sequence,
    or as positional arguments.

    In other words, it makes it possible to use
    the following two forms of invocation::

        func([1, 2, 3])
        func(1, 2, 3)

    In both cases `func` receives 1, 2 and 3 as
    positional arguments (`*args`).
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
            arg_collection = (isinstance(arg, Iterable)
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
    """Generator that returns a random element from given set.

    Elements can be passed either directly as arguments::

        elements(1, 2, 3)

    or as a list::

        elements([1, 2, 3]) 

    Every element has equal probability of being chosen.
    """
    if not args:
        raise ValueError("cannot pick random element from empty sequence")
    return random.choice(args)


@combinator
def one_of(*args):
    """Generator that yields values coming from given set of generators.

    Generators can be passed either directly as arguments::

        one_of(int, float)

    or as a list::

        one_of([int, float])

    Every generator has equal probability of being chosen.
    If you need to have a non-uniform probability distribution,
    use the :func:`frequency` function.
    """
    if not args:
        raise ValueError("no generators to choose from")
    return next(random.choice(args))


@combinator
def frequency(*args):
    """Generator that yields coming from given set of generators,
    according to their probability distribution.

    The distribution is just a set of tuples: `(gen, freq)`
    which can be passed either directly as arguments::

        frequency((int, 1), (float, 2))

    or a a list::

        frequency([(int, 1), (float, 2)])

    The second element of tuple (`freq`) is the relative frequency
    of values from particular generator, compared to those from other
    generators. In both examples above the resulting generator will
    yield `float`\ s twice as often as `int`\ s.

    Typically, it's convenient to use floating-point frequencies
    that sum to 1.0 or integer frequencies that sum to 100.
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
