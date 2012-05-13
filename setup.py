#!/usr/bin/env python
"""
pyqcy
=====

*pyqcy* [pyksi:] is an automated testing framework for Python
inspired by the wonderful *QuickCheck* library for Haskell.

What's the idea?
----------------

Instead of writing fully-fledged test cases, with *pyqcy*
you simply define logical **properties** that your code
is expected to satisfy. Based on that, *pyqcy* will
automatically generate test cases for you - hundreds of them,
in fact!

How does it look like?
----------------------

For starters, try this::

    from pyqcy import qc, int_, main

    @qc
    def addition_actually_works(
        x=int_(min=0), y=int_(min=0)
    ):
        the_sum = x + y
        assert the_sum >= x and the_sum >= y

    if __name__ == '__main__':
        main()

::

    $ pip install pyqcy
    $ python test.py
    addition_actually_works: passed 100 tests.

*pyqcy* generated 100 test cases and checked whether
they all pass. For a few lines of code, that's rather nice,
isn't it? :)

Of course, you are not limited to integers - there is
built-in support for all standard types, including lists
and dictionaries. Custom classes can be used as well:
just specify how to generate an *@arbitrary* object
of your class, and you're set.

Hey, I like it!
---------------

Then check these links to find out more:

* `website <http://xion.io/pyqcy>`_
* `documentation <http://pyqcy.readthedocs.org>`_
* `github <http://github.com/Xion/pyqcy>`_
"""
from setuptools import setup, find_packages

import pyqcy


setup(
    name="pyqcy",
    version=pyqcy.__version__,
    description="QuickCheck-like testing framework for Python",
    long_description=__doc__,
    author='Karol Kuczmarski "Xion"',
    author_email="karol.kuczmarski@gmail.com",
    url="http://xion.io/pyqcy",
    license="Simplified BSD",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],

    platforms='any',
    packages=find_packages(),
    tests_require=['nose'],
)
