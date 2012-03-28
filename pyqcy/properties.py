"""
Properties to be tested.
Also known as "tests".
"""
import inspect
import functools

from .arbitraries import arbitrary


__all__ = ['qc']


DEFAULT_TEST_COUNT = 100

class Property(object):
	"""A property that can be QuickChecked.
	"""
	def __init__(self, args, kwargs, func):
		"""Constructor. Callers should specify the function
		which encodes the testing property, and arbitrary values'
		generator for both positonal and keyword arguments.
		"""
		self.args = map(self.__coerce_to_arbitrary, args)
		self.kwargs = dict((k, self.__coerce_to_arbitrary(v))
						   for k, v in kwargs.iteritems())
		self.func = self.__coerce_to_generator_func(func)

	def __coerce_to_arbitrary(self, obj):
		"""Ensures that given object is a generator of arbitrary values.
		Rather than permitting only actual generators, this allows
		us to pass generator functions or even types, provided
		there is a know arbitrary generator for them.
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
			return self.__coerce_to_arbitrary(arbit_gens[0])

		raise ValueError(
			"invalid generator of arbitrary values: %r (of type %s)" % (
				obj, type(obj).__name__))

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

	def test_one(self):
		"""Executes a single test for this property."""
		args = self.__arbitrary_args()
		kwargs = self.__arbitrary_kwargs()
		coroutine = self.func(*args, **kwargs)
		self.__execute_test(coroutine)

	def test(self, count=DEFAULT_TEST_COUNT):
		"""Executes given number of tests for this property
		and gathers statistics about all test runs.
		"""
		# no statistics yet
		for _ in xrange(count):
			self.test_one()

	__call__ = test

	def __arbitrary_args(self):
		"""Returns a list of arbitrary values for
		positional arguments of the property function.
		"""
		return map(next, self.args)

	def __arbitrary_kwargs(self):
		"""Returns a dictionary of arbitrary values
		for keyword arguments of the property function.
		"""
		return dict((k, next(v)) for k, v in self.kwargs.iteritems())

	def __execute_test(self, coroutine):
		"""Executes given test coroutine and returns results,
		such as classifiers or collected values.
		"""
		try:
			# so far it's simple, no stats
			while True:
				next(coroutine)
		except StopIteration:
			pass


# The @qc decorator

class PropertyDecorator(object):
	"""Class used to implement the @qc decorator
	which is to be applied on properties.
	"""
	def __init__(self, *args, **kwargs):
		self.prop_args = args
		self.prop_kwargs = kwargs

	def __call__(self, func):
		return Property(self.prop_args, self.prop_kwargs, func)


def qc(first_arg=None, *args, **kwargs):
	"""@qc decorator to be applied on functions that encode
	QuickCheck properties to be tested.
	"""
	# applying @qc on function whose default arguments
	# specify generators of arbitrary values for those arguments
	parameterless_applicaton = (
		inspect.isfunction(first_arg) and
		not getattr(first_arg, '_arbitrary', False) and
		not (args or kwargs)
	)
	if parameterless_applicaton:
		func_args, _, _, func_defaults = inspect.getargspec(first_arg)
		free_args_count = len(func_args) - len(func_defaults)
		if free_args_count > 0:
			raise TypeError("property has unbound variables: %s" %
				func_args[:free_args_count])
		return Property(args=func_defaults, kwargs={}, func=first_arg)

	# typical application, e.g.: @qc(x=int_, y=float_)
	if first_arg is not None:
		args = [first_arg] + list(args)
	return PropertyDecorator(*args, **kwargs)
