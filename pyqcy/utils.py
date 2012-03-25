"""
Utility module.
"""
import functools
import inspect


def optional_args(decor):
	"""Decorator for decorators (sic) that are intended to take
	optional arguments. It supports decorators written both as
	classes or functions, as long as they are "doubly-callable".
	For classes, this means implementing `__call__`, while
	functions must return a function that returns a function
	that accepts a function... which is obvious, of course.
	"""
	@functools.wraps(decor)
	def wrapped(*args, **kwargs):
		one_arg = len(args) == 1 and not kwargs
		if one_arg and inspect.isfunction(args[0]):
			decor_instance = decor()
			return decor_instance(args[0])
		else:
			return decor(*args, **kwargs)

	return wrapped