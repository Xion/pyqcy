# pyqcy

_QuickCheck_-like testing framework for Python

## What, another testing utility?

It's true that Python has plethora of testing tools, especially when it comes to
[unit tests](http://packages.python.org/testing/#unit-testing-tools). Why would
anyone want another library dedicated to that?...

For one, _pyqcy_ (\[pyksi:\]) supports a unique testing model, based on the
brilliant _QuickCheck_ library for Haskell. Rather than writing fully-fledged
test cases, you only need to define logical **properties** that your code
has to satisfy. Based on that, _pyqcy_ will automatically generate test cases
- hundreds of them, in fact!

## So, how does it look like?

Try this:

    #!python
    from pyqcy import qc, main

    @qc
    def addition_actually_works(x=int, y=int):
    	the_sum = x + y
    	assert sum >= x and sum >= y

    if __name__ == '__main__':
    	main()

It will print:

    addition_actually_works: passed 100 tests.

That's one hundred test cases generated automatically. In this example
with <code>int</code> sit is of course very simple, but _pyqcy_ already
has support for most Python types, including strings and lists.
Futhermore it also allows you to define your own generators
using the <code>@arbitrary</code> decorator.

See _tests.py_ for more usage examples.

## How far does it go?

Although quite functional (pun likely intended), this project is in experimental phase.
The aim is to make very similar to Haskell's _QuickCheck_, in extent
permitted by the dynamic nature of Python.

Ideas, suggestions and contributions are very welcome.
