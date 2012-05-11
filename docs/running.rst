Running the tests
=================

Once you have written some tests using *pyqcy*, you would probably want run them.
Dependning on whether you already have a test suite of different kinds
of tests (most typically unit tests), you may want to integrate *pyqcy* properties
into that. Alternatively, properties can be also verified using a built-in, standalone
test runner.


Test runner
-----------

*pyqcy* includes a readily available test runner which can be used to run verification
tests for all properties defined within given module. For it to work, you just need
to include a traditional `if __name__ == '__main__':` boilerplate which calls `pyqcy.main`:

.. code-block:: python

    from pyqcy import *

    # ... define test properties here ...

    if __name __ == '__main__':
        main()

This default test runner will go over all properties defined within this module,
as well as all modules it imports, and execute tests for them. It is intentionally
similar in usage to standard `unittest.main` and shares many parameters with the
`unittest` runner (to the extent it makes sense for *pyqcy* tests, of course).


.. autofunction:: pyqcy.runner.main


Integration with testing frameworks
-----------------------------------

If you are already using a framework for running unit tests against your project,
you can probably integrate *pyqcy* property tests into it in very easy way.

For the purposes of such integration, *pyqcy* defines the :class:`TestCase` class
that is a direct descendant from the standard `unittest.TestCase`. Because of that,
test cases built upon it will be gathered and ran by pretty much any testing framework
- be it `unittest` itself, *nose*, *py.test*, etc.

Therefore all we need to do for our properties to be picked up is to put them inside
a :class:`TestCase` subclass::

    from pyqcy import *

    class Arithmetic(TestCase):
        @qc
        def addition_on_ints(x=int, y=int):
            assert isinstance(x + y, int)
        @qc
        def subtraction_on_ints(x=int, y=int):
            assert isinstance(x - y, int)

There is no need to rename the properties to start with `test_` but we should retain
the :func:`qc` decorator. We also don't need to include any other methods to run
our property tests explicitly; the base :class:`TestCase` class will take care of it
automatically.

.. autoclass:: pyqcy.integration.TestCase
