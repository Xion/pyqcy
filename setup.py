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
import ast
import os
from setuptools import setup, find_packages


def read_tags(filename):
    """Reads values of "magic tags" defined in the given Python file.

    :param filename: Python filename to read the tags from
    :return: Dictionary of tags
    """
    with open(filename) as f:
        ast_tree = ast.parse(f.read(), filename)

    res = {}
    for node in ast.walk(ast_tree):
        if type(node) is not ast.Assign:
            continue

        target = node.targets[0]
        if type(target) is not ast.Name:
            continue

        if not (target.id.startswith('__') and target.id.endswith('__')):
            continue

        name = target.id[2:-2]
        res[name] = ast.literal_eval(node.value)

    return res


def read_requirements(filename='requirements.txt'):
    """Reads the list of requirements from given file.

    :param filename: Filename to read the requirements from.
                     Uses ``'requirements.txt'`` by default.

    :return: Requirements as list of strings
    """
    # allow for some leeway with the argument
    if not filename.startswith('requirements'):
        filename = 'requirements-' + filename
    if not os.path.splitext(filename)[1]:
        filename += '.txt'  # no extension, add default

    def valid_line(line):
        line = line.strip()
        return line and not any(line.startswith(p) for p in ('#', '-'))

    def extract_requirement(line):
        egg_eq = '#egg='
        if egg_eq in line:
            _, requirement = line.split(egg_eq, 1)
            return requirement
        return line

    with open(filename) as f:
        lines = f.readlines()
        return list(map(extract_requirement, filter(valid_line, lines)))


tags = read_tags(os.path.join('pyqcy', '__init__.py'))
__doc__ = __doc__.format(**tags)


setup(
    name="pyqcy",
    version=tags['version'],
    description=tags['description'],
    long_description=__doc__,
    author=tags['author'],
    author_email=tags['author_email'],
    url="http://xion.io/pyqcy",
    license=tags['license'],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
    ],

    platforms='any',
    packages=find_packages(),
    tests_require=read_requirements('test'),
)
