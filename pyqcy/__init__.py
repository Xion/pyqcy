"""
pyqcy
"""
__version__ = "0.4.5"
__description__ = "QuickCheck-like testing framework for Python"
__author__ = 'Karol Kuczmarski "Xion"'
__author_email__ = "karol.kuczmarski@gmail.com"
__license__ = "Simplified BSD"


from .arbitraries import *
from .properties import *
from .results import *
from .statistics import *

from .integration import *
from .runner import *
