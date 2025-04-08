"""Impact Indicator Categories"""

from dataclasses import dataclass

from ...decisions.default import EnvImp, SocImp
from .indicator import Indicator


@dataclass
class Env(Indicator, EnvImp):
    """Environmental Impact"""


@dataclass
class Soc(Indicator, SocImp):
    """Soc Impact"""


@dataclass
class Eco(Indicator):
    """Economic impact"""
