"""Impact Indicator Categories"""

from dataclasses import dataclass

from .indicator import Indicator

from ...decisions.default import SocImp, EnvImp


@dataclass
class Environ(Indicator, EnvImp):
    """Environmental Impact"""


@dataclass
class Social(Indicator, SocImp):
    """Social Impact"""


@dataclass
class Econ(Indicator):
    """Economic impact"""
