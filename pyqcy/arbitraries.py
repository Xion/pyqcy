"""
Generators of arbitrary values.
"""
import functools
import random
import sys

from .utils import optional_args


__all__ = ['arbitrary']


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
			return self.__normal_generator_function(func)
		else:
			gen =  self.__validating_generator_function(func)

			self.registry.setdefault(self.type_, [])
			self.registry[self.type_].append(gen)
			return gen

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


# Arbitrary values' generators for built-in types

@arbitrary(int)
def int_():
	return random.randint(0, sys.maxint)

@arbitrary(float)
def float_():
	return random.random() * sys.maxint

@arbitrary(complex)
def complex_():
	floats = float_()
	return complex(next(floats), next(floats))
