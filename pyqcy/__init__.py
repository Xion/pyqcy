"""
pyqcy :: QuickCheck-like testing framework for Python
"""
import functools
import inspect

from .utils import optional_args


__all__ = ['arbitrary', 'qc']


## Arbitraries (generators)

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
		"""A generator that  endlessly spits out results of calling
		a single parameterless function.
		"""
		while True:
			yield func()


## Properties ("tests")

DEFAULT_TEST_COUNT = 100

class QcProperty(object):
	"""A property that can be QuickChecked.
	"""
	def __init__(self, prop_args, prop_kwargs, prop_func):
		self.args = prop_args
		self.kwargs = prop_kwargs
		self.func = self.__coerce_to_generator_func(prop_func)

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

	def __call__(self, count=DEFAULT_TEST_COUNT):
		"""Calling a property executes given number of tests. """
		# no statistics yet
		for _ in xrange(count):
			self.test()

	def test(self):
		"""Executes a single test for this property."""
		args = self.__arbitrary_args()
		kwargs = self.__arbitrary_kwargs()
		coroutine = self.func(*args, **kwargs)
		self.__execute_test(coroutine)

	def __arbitrary_args(self):
		"""Returns a list of arbitrary values for positional arguments
		for the property function.
		"""
		return map(next, self.args)

	def __arbitrary_kwargs(self):
		"""Returns a dictionary of arbitrary values for keyword arguments
		for the property function.
		"""
		return dict((k, next(v)) for k, v in self.kwargs.iteritems())

	def __execute_test(self, coroutine):
		"""Executes given test coroutine and returns results,
		such as classifiers or collected values.
		"""
		try:
			# so far it's simple
			while True:
				next(coroutine)
		except StopIteration:
			pass


class qc(object):
	"""@qc decorator to be applied on functions that encode
	QuickCheck properties to be tested.
	"""
	def __init__(self, *args, **kwargs):
		self.prop_args = args
		self.prop_kwargs = kwargs

	def __call__(self, func):
		return QcProperty(self.prop_args, self.prop_kwargs, func)
