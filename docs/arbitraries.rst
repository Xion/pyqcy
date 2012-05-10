Using generators
================


Built-in types
**************

.. currentmodule:: pyqcy.arbitraries.standard


Scalar types
------------

.. autofunction:: int_(min, max)

.. autofunction:: float_(min, max)

.. autofunction:: complex_(min_real, max_real, min_imag, max_imag)

.. autofunction:: str_(of, min_length, max_length)


Tuples
------

.. autofunction:: tuple_(*generators, of, n)

.. autofunction:: two(of)

.. autofunction:: three(of)

.. autofunction:: four(of)


Collections
-----------

.. autofunction:: list_(of, min_length, max_length)

.. autofunction:: dict_(keys, values, items, min_length, max_length)


Combinators
***********

.. currentmodule:: pyqcy.arbitraries.combinators

.. autofunction:: one_of(*generators)

.. autofunction:: frequency(*distribution)

.. autofunction:: elements(*list)


Data structures
---------------

.. autofunction:: data


Applying functions
------------------

.. autofunction:: apply
