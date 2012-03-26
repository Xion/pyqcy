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
	def __init__(self, type_=None):
		self.type_ = type_

	def __call__(self, func):
		if self.type_ is None:
			return self.__normal_generator(func)
		else:
			return self.__validating_generator(func)

	def __normal_generator(self, func):
		"""Returns a version of arbitrary generator
		that does not validate output value.
		"""
		return self.__yielder(func)

	def __validating_generator(self, func):
		"""Returns a version of arbitrary generator
		that validates output value against type given
		as @arbitrary parameter.
		"""
		@functools.wraps(func)
		def wrapped():
			value = func()
			if not isinstance(value, self.type_):
				raise TypeError(
					"arbitrary value %r is of type %s; expected %s" % (
						value, type(value).__name__, self.type_.__name__))
			return value
		return self.__yielder(wrapped)

	def __yielder(self, func):
		"""A generator that endlessly spits out results of calling
		a single parameterless function.
		"""
		while True:
			yield func()


# Arbitrary values' generators for built-in types

@arbitrary(int)
def _int():
	return random.randint(0, sys.maxint)