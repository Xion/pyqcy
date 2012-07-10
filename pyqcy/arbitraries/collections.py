"""
Generators for arbitrary collections (tuples, lists, dictionaries).
"""
import random
import functools

from pyqcy.arbitraries import arbitrary, is_arbitrary


@arbitrary
def tuple_(*args, **kwargs):
    """Generator for arbitrary tuples.

    The tuples are always of the same length but their values
    may come from different generators. There two ways to specify
    those generators - either enumerate them all::

        tuple_(int_(min=0, max=255), str_(max_length=64))

    or use ``n`` argument with a single generator to get uniform tuples::

        ip_addresses = tuple_(int_(min=0, max=255), n=4)
        ip_addresses = tuple_(of=int_(min=0, max=255), n=4)

    Those two styles are mutually exclusive - only one can be used at a time.

    :param of: Generator used to generate tuple values
    :param n: Tuple length
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


#: Generator for arbitrary pairs, combining two values
#: coming from a single generator into tuple of length 2.
two = functools.partial(tuple_, n=2)

#: Generator for arbitrary triples, combining two values
#: coming from a single generator into tuple of length 3.
three = functools.partial(tuple_, n=3)

#: Generator for arbitrary quadruples, combining two values
#: coming from a single generator into tuple of length 4.
four = functools.partial(tuple_, n=4)


@arbitrary
def list_(of, min_length=0, max_length=1024):
    """Generator for arbitrary lists.

    Parameters for this generator allow for adjusting the length
    of resulting list and elements they contain.

    :param of: Generator for list elements
    :param min_length: A minimum length of list to generate
    :param max_length: A maximum length of list to generate

    Example of test property that uses :func:`list_`::

        @qc
        def calculating_average(
            l=list_(of=int_(min=0, max=1024),
                    min_length=16, max_length=2048)
        ):
            average = sum(l) / len(l)
            assert min(l) <= average <= max(l)
    """
    length = random.randint(min_length, max_length)
    if is_arbitrary(of):
        return [next(of) for _ in xrange(length)]
    return [random.choice(of) for _ in xrange(length)]


@arbitrary
def dict_(keys=None, values=None, items=None,
          min_length=0, max_length=1024):
    """Generator for arbitrary dictionaries.

    Dictionaries are specified using generators - either for
    ``keys`` and ``values`` separately::

        dict_(keys=str_(max_length=64), values=str_(max_length=64))

    or already combined into ``items`` (which should yield key-value pairs)::

        dict_(items=two(str_(max_length=64)))

    Those two styles are mutually exclusive - only one can be used at a time.

    :param keys: Generator for dictionary keys
    :param values: Generator for dictionary values
    :param items: Generator for dictionary items (2-element tuples).
    :param min_length: A minimum number of items
                       the resulting dictionary will contain
    :param max_length: A maximum number of items
                       the resulting dictionary will contain
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
