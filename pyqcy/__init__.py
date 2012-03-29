"""
pyqcy :: QuickCheck-like testing framework for Python
"""
from .arbitraries import *
from .properties import *


def main(module='__main__'):
	"""Test runner. When called, it will look for all properties
	(i.e. functions with @qc decorator) and push them through
	a default number of checks.
	Arguments are intended to mimic those from unittest.main().
	Return value is the total number of properties checked.
	"""
	if isinstance(module, basestring):
		module_name = module
		module = __import__(module_name)
		for part in module_name.split('.')[1:]:
			module = getattr(module, part)

	from .properties import Property, DEFAULT_TEST_COUNT

	props = [v for v in module.__dict__.itervalues()
			 if isinstance(v, Property)]
	for p in props:
		p.test()
		print "%s: passed %s test%s." % (p.func.__name__,
			DEFAULT_TEST_COUNT,
			"s" if DEFAULT_TEST_COUNT != 1 else "")
		
	return len(props)
	