"""
pyqcy :: QuickCheck-like testing framework for Python
"""
__version__ = "0.4.5"
__author__ = 'Karol Kuczmarski "Xion"'
__license__ = "BSD"


from .arbitraries import *
from .properties import *
from .results import *
from .statistics import *

from .integration import *
from .runner import *
