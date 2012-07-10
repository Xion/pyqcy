Gathering statistics
====================

.. currentmodule:: pyqcy.statistics

As your tests :doc:`are ran <running>`, you may want to gain some insight
into what test cases are actually generated in order to verify your properties.
Usually, however, there will be hundreds or thousands of them, so you
certainly don't want to wade through them all.

To consolidate this data into more useful information, *pyqcy* provides you
with statistical functions: :func:`collect` and :func:`classify`.


.. warning::
   All statistical functions described below must be ``yield`` from within
   test properties to be recorded.

.. autofunction:: collect

.. autofunction:: classify
