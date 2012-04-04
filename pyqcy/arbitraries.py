"""
Generators of arbitrary values.
"""
import functools
import inspect
import random
import sys

from .utils import optional_args


@optional_args
class arbitrary(object):
	"""@arbitrary decorator which can be applied on functions
	that are intended to output "random" (arbitrary) values
	of given type.
	"""
	# Dictionary mapping types into
	# generators of arbitrary values for those types
	registry = {}

	def __init__(self, type_=None):
		self.type_ = type_

	def __call__(self, func):
		"""Applies the @arbitrary decorator to given function.
		If `type` argument was supplied previously,
		the resulting generator will be remembered in global registry
		for easy reference.
		"""
		if self.type_ is None:
			gen_func = self.__arbitrary_generator(func)
		else:
			def validate(value):
				if not isinstance(value, self.type_):
					raise TypeError(
						"arbitrary value %r is of type %s; expected %s" % (
							value, type(value).__name__, self.type_.__name__))
				return value

			gen_func =  self.__arbitrary_generator(func, validate)
			self.registry.setdefault(self.type_, [])
			self.registry[self.type_].append(gen_func)

		gen_func._arbitrary = True # marker attribute
		return gen_func

	def __arbitrary_generator(self, func, value_func=None):
		"""Constructs arbitrary generator based on given function `func`.
		It can be both a function that returns a single value,
		or a generator function.
		"""
		if value_func is None:
			value_func = lambda v: v # identity function

		if inspect.isgeneratorfunction(func):
			@functools.wraps(func)
			def wrapper(*args, **kwargs):
				args, kwargs = self.__coerce_to_arbitraries(args, kwargs)
				for obj in func(*args, **kwargs):
					yield value_func(obj)
		else:
			@functools.wraps(func)
			def wrapper(*args, **kwargs):
				args, kwargs = self.__coerce_to_arbitraries(args, kwargs)
				while True:
					yield value_func(func(*args, **kwargs))

		return wrapper

	def __coerce_to_arbitraries(self, args=[], kwargs={}):
		"""Ensures given list and dictionary of positional and keyword
		arguments contains appropriate arbitrary values' generators.
		Elements that cannot be reasonably coerced into arbitraries
		are left unchanged.
		"""
		args = [to_arbitrary(arg) if is_arbitrary(arg) else arg
				for arg in args]
		kwargs = dict((k, to_arbitrary(v) if is_arbitrary(v) else v)
					  for (k, v) in kwargs.iteritems())
		return args, kwargs


def is_arbitrary(obj):
	"""Checks whether given object can work as generator of arbitrary values.
	This functions handles all the forms in which arbitraries can occur
	in the code, including: generators, generator functions, and types.
	"""
	if inspect.isgenerator(obj):
		return True
	if inspect.isgeneratorfunction(obj):
		return getattr(obj, '_arbitrary', False)
	if isinstance(obj, type):
		return obj in arbitrary.registry
	return False

def to_arbitrary(obj):
	"""Ensures that given object is a generator of arbitrary values.
	Rather than permitting only actual generators, this allows
	us to pass generator functions or even types, provided
	there is a known arbitrary generator for them.
	"""
	if inspect.isgenerator(obj):
		return obj
	if inspect.isgeneratorfunction(obj):
		return obj()	# fails if arguments are required,
						# and this is intended

	# looking up types in global registry
	if isinstance(obj, type):
		arbit_gens = arbitrary.registry.get(obj)
		if not arbit_gens:
			raise TypeError(
				"no arbitrary values' generator found for type: %s" % obj)
		return to_arbitrary(arbit_gens[0])

	raise ValueError(
		"invalid generator of arbitrary values: %r (of type %s)" % (
			obj, type(obj).__name__))


# Arbitrary values' generators for built-in scalar types

@arbitrary(int)
def int_(min=0, max=sys.maxint):
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
	return ''.join(chr(next(of)) for _ in xrange(length))

# Arbitrary values' generators for built-in collection types

@arbitrary
def tuple_(*args):
	"""Generator for arbitrary tuples. Resulting tuples are always
	of same length, equal to number of arbitrary generators passed
	to this function.
	"""
	return tuple(map(next, args))
	
@arbitrary
def list_(of, min_length=0, max_length=1024):
	"""Generator for arbitrary lists. List elements themselves
	can come from any arbitrary generator passed as first argument.
	"""
	length = random.randint(min_length, max_length)
	return [next(of) for _ in xrange(length)]
	
@arbitrary
def dict_(keys=None, values=None, items=None,
		  min_length=0, max_length=1024):
	"""Generator for arbitrary dictionaries. Either `keys` and `values`,
	or the `items` argument must be provided - but not both.
	"""
	if not ((keys and values) or items):
		raise ValueError("invalid dictionary items' generators provided")

	next_item = ((lambda: next(items)) if items else
				 (lambda: (next(keys), next(values))))
	length = random.randint(min_length, max_length)
	return dict(next_item() for _ in xrange(length))
