"""Player"""

from dataclasses import dataclass

from ...decisions.default import Capacitate, Trade, Transact
from ..core.modeling import Component


@dataclass
class Player(Component, Capacitate, Trade, Transact):
    """Player or Actor, the one taking the decisions
    based on information provided

    Players own certain processes and be responsible for the flows and impact
    caused by their decisions pertaining to this
    """

    def __post_init__(self):
        Component.__post_init__(self)
