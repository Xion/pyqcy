"""
Simple, built-in test runner.
"""
import sys
import os
import traceback


def main(module='__main__', exit=True, failfast=False):
	"""Test runner. When called, it will look for all properties
	(i.e. functions with @qc decorator) and push them through
	a default number of checks.
	Arguments are intended to mimic those from unittest.main().
	Return value is the total number of properties checked
	(provided the exit=False and program doesn't terminate).
	"""
	if isinstance(module, basestring):
		module_name = module
		module = __import__(module_name)
		for part in module_name.split('.')[1:]:
			module = getattr(module, part)

	from .properties import Property, DEFAULT_TEST_COUNT
	props = [v for v in module.__dict__.itervalues()
			 if isinstance(v, Property)]

	# run the tests
	failed = False
	for p in props:
		try:
			p.test()
		except:
			print "%s: failed." % p.func.__name__
			traceback.print_exception(*sys.exc_info())
			failed = True
			if failfast:
				break
		else:	
			print "%s: passed %s test%s." % (p.func.__name__,
				DEFAULT_TEST_COUNT,
				"s" if DEFAULT_TEST_COUNT != 1 else "")
		
	if exit:
		sys.exit(1 if failed else 0)
	return len(props)
	