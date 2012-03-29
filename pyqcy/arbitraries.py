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
			gen_func = self.__normal_generator_function(func)
		else:
			gen_func =  self.__validating_generator_function(func)

			self.registry.setdefault(self.type_, [])
			self.registry[self.type_].append(gen_func)

		gen_func._arbitrary = True
		return gen_func

	def __normal_generator_function(self, func):
		"""Returns a version of arbitrary generator function
		that does not validate output value.
		"""
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			while True:
				yield func(*args, **kwargs)

		return wrapper

	def __validating_generator_function(self, func):
		"""Returns a version of arbitrary generator function
		that validates output value against type given
		as @arbitrary parameter.
		"""
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			while True:
				value = func(*args, **kwargs)
				if not isinstance(value, self.type_):
					raise TypeError(
						"arbitrary value %r is of type %s; expected %s" % (
							value, type(value).__name__, self.type_.__name__))
				yield value

		return wrapper


def isarbitrary(obj):
	"""Checks whether given object is a generator of arbitrary values.
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


# Arbitrary values' generators for built-in types

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
	
@arbitrary
def list_(of, min_length=0, max_length=1024):
	"""Generator for arbitrary lists. List elements themselves
	can come from any arbitrary generator passed as first argument.
	"""
	length = random.randint(min_length, max_length)
	return [next(of) for _ in xrange(length)]
	