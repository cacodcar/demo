"""Impact Indicator Categories"""

from dataclasses import dataclass
from .indicator import Indicator


@dataclass
class Environ(Indicator):
    """Environmental Impact"""


@dataclass
class Social(Indicator):
    """Social Impact"""


@dataclass
class Econ(Indicator):
    """Economic impact"""
