# pyqcy

_QuickCheck_-like testing framework for Python

[![Build Status](https://secure.travis-ci.org/Xion/pyqcy.png)](http://travis-ci.org/Xion/pyqcy)

## What, another testing utility?

It's true that Python has plethora of testing tools, especially when it comes to
[unit tests](http://packages.python.org/testing/#unit-testing-tools). So why would
anyone want another library dedicated to this end?...

For one, _pyqcy_ \[pyksi:\] supports a unique testing model, inspired by the
brilliant _QuickCheck_ library for Haskell. Rather than writing fully-fledged
test cases, you only need to define logical **properties** that your code
has to satisfy. Based on that, _pyqcy_ will automatically generate test cases -
hundreds of them, in fact!

## So, how does it look like?

Install _pyqcy_:

    $ pip install pyqcy

and then try this:

```python
from pyqcy import qc, int_, main

@qc
def addition_actually_works(
	x=int_(min=0), y=int_(min=0)
):
	the_sum = x + y
	assert the_sum >= x and the_sum >= y

if __name__ == '__main__':
	main()
```
It will print:

    $ python ./example.py
    addition_actually_works: passed 100 tests.

That's one hundred test cases generated automatically. In this example
with <code>int</code>s it is of course very simple, but _pyqcy_ already
has support for most Python types, including strings and lists.
Futhermore it also allows you to define your own generators
using the <code>@arbitrary</code> decorator.

See the _tests_ package for more usage examples.

## How far does it go?

Check out [the docs](http://pyqcy.readthedocs.org) for comprehensive explanation
of features currently offered by _pyqcy_.

The aim of this project is to make it very similar to Haskell's _QuickCheck_,
in extent permitted by the dynamic nature of Python. So far it turned out to be
quite big extent :)

## Cool! Can I help?

Sure thing! Ideas, suggestions and of course contributions are all very welcome.

If you want to start hacking at _pyqcy_ right away, just clone it from here
and install in development mode (preferably inside a virtualenv):

    $ git clone git://github.com/Xion/pyqcy.git
    $ cd pyqcy
    $ python ./setup.py develop

Then you should be able to run tests through _nose_:

    $ pip install nose
    $ nosetests
