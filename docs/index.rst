.. pyqcy documentation master file, created by
   sphinx-quickstart on Sat May  5 00:30:04 2012.

pyqcy
=====

*pyqcy* [pyksi:] is a test framework that supports unique testing model, inspired by the brilliant
*QuickCheck* library for Haskell. Rather than writing fully-fledged test cases, you only need to
define logical **properties** that your code has to satisfy. Based on that, *pyqcy* will automatically
generate test cases for you - hundreds of them, in fact!


Example
-------

.. code-block:: python

    from pyqcy import qc, int_ main

    @qc
    def addition_actually_works(
        x=int_(min=0), y=int_(min=0)
    ):
        the_sum = x + y
        assert the_sum >= x and the_sum >= y

    if __name__ == '__main__':
        main()

.. code-block:: console

    $ python ./example.py
    addition_actually_works: passed 100 tests.

Yes, that's 100 distinct test cases. *pyqcy* has generated them all for you!


Installation
------------

Either from PyPI:

.. code-block:: console

    $ pip install pyqcy

or directly from GitHub if you want the bleeding edge version:

.. code-block:: console

    $ git clone git://github.com/Xion/pyqcy.git
    $ cd pyqcy
    $ ./setup.py develop


Learn more
----------

.. toctree::
   :maxdepth: 1

   Defining properties <properties>
   Using generators <arbitraries>
   Gathering statistics <statistics>
   Running the tests <running>
