"""
pyqcy :: QuickCheck-like testing framework for Python
"""
__version__ = "0.3.2"
__author__ = "Karol Kuczmarski"
__license__ = "BSD"


from .arbitraries import *
from .properties import *
from .statistics import *

from .integration import *
from .runner import *
