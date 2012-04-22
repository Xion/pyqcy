"""
Arbitrary values generators
for standard Python types.
"""
import sys
import random
import functools

from pyqcy.arbitraries import arbitrary, is_arbitrary


# Arbitrary values' generators for built-in scalar types

@arbitrary(int)
def int_(min=-sys.maxint - 1, max=sys.maxint):
    """Default arbitrary values' generator for the int type."""
    return random.randint(min, max)


@arbitrary(float)
def float_(min=-float(sys.maxint), max=float(sys.maxint)):
    """Default arbitrary values' generator for the float type."""
    return min + random.random() * (max - min)


@arbitrary(complex)
def complex_(min_real=-float(sys.maxint), max_real=float(sys.maxint),
             min_imag=-float(sys.maxint), max_imag=float(sys.maxint)):
    """Default arbitrary values' generator for the complex type."""
    reals = float_(min_real, max_real)
    imags = float_(min_imag, max_imag)
    return complex(next(reals), next(imags))


@arbitrary(str)
def str_(of=int_(min=0, max=255), min_length=1, max_length=64):
    """Default arbitrary values' generator for strings."""
    length = random.randint(min_length, max_length)
    if is_arbitrary(of):
        return ''.join(chr(next(of)) for _ in xrange(length))
    return ''.join(random.choice(of) for _ in xrange(length))


# Arbitrary values' generators for built-in collection types

@arbitrary
def tuple_(*args, **kwargs):
    """Generator for arbitrary tuples. Resulting tuples are always
    of same length, equal to number of arbitrary generators passed
    to this function or the value of `n` keyword argument.
    """
    n = kwargs.get('n')
    if n is None:
        return tuple(map(next, args))

    of = kwargs.get('of')
    if of:
        if args:
            raise TypeError("ambiguous invocation - "
                            "more than one possible type for tuple elements")
    else:
        if len(args) != 1:
            raise TypeError("no/invalid type of arbitrary tuple elements")
        of = args[0]

    return tuple(next(of) for _ in xrange(n))


two = functools.partial(tuple_, n=2)
three = functools.partial(tuple_, n=3)
four = functools.partial(tuple_, n=4)


@arbitrary
def list_(of, min_length=0, max_length=1024):
    """Generator for arbitrary lists. List elements themselves
    can come from any arbitrary generator passed as first argument.
    """
    length = random.randint(min_length, max_length)
    if is_arbitrary(of):
        return [next(of) for _ in xrange(length)]
    return [random.choice(of) for _ in xrange(length)]


@arbitrary
def dict_(keys=None, values=None, items=None,
          min_length=0, max_length=1024):
    """Generator for arbitrary dictionaries. Either `keys` and `values`,
    or the `items` argument must be provided - but not both.
    """
    kv_provided = keys is not None and values is not None
    items_provided = items is not None
    if not (kv_provided or items_provided):
        raise ValueError("no generators for dictionary items provided")
    if kv_provided and items_provided:
        raise ValueError("ambiguous invocation - "
                         "provide either keys and values, or items")

    next_item = ((lambda: next(items)) if items_provided else
                 (lambda: (next(keys), next(values))))
    length = random.randint(min_length, max_length)
    return dict(next_item() for _ in xrange(length))
