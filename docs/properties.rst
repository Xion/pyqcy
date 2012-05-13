Defining properties
===================

In *pyqcy*, the test properties are defined as regular Python functions
but they are all adorned with the :func:`qc` decorator.

Here's an example:

.. code-block:: python

	from pyqcy import *

	@qc
	def sorting_preserves_length(
	    l=list_(of=int, min_length=1, max_length=128)
	):
	    before_sort = l
	    after_sort = list(sorted(l))
	    assert len(before_set) == len(after_sort)

Inside the function, we use its parameters as a sort of **quantified variables**.
As you can see, their defaults are somewhat unusual as they specify how to
obtain *arbitrary* (i.e. random) values for those variables. *pyqcy* will take
those :doc:`specifications <arbitraries>`, use them to automatically generate test data
and then invoke your property's code.

.. note::
	For more information about different way of running tests for your properties,
	check the :doc:`documentation on that <running>`.


.. autofunction:: pyqcy.qc([tests])

	:param tests: Number of tests to execute for this property.
				  If omitted, the default number of 100 tests will be executed.
				  