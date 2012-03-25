#!/usr/bin/env python
"""
Setup file for pyqcy package
"""
from setuptools import setup, find_packages


setup(
	name="pyqcy",
	version="0.1",
	description="QuickCheck-like testing framework for Python",
	author='Karol Kuczmarski "Xion"',
	author_email="karol.kuczmarski@gmail.com",
	url="http://github.com/Xion/pyqcy",
	license="BSD",

	classifiers = [
		"Development Status :: 2 - Pre-Alpha",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
        "Programming Language :: Python",
	],

	packages=find_packages(),
)