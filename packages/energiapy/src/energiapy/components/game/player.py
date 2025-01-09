"""Player"""

from dataclasses import dataclass
from .._core.modeling import Component

from ...decisions.action import Add
from ..spatial.inventory import Inv
from ..commodity.resource import Resource


@dataclass
class Player(Component):
    """Player or Actor, the one taking the decisions
    based on information provided

    Players own certain processes and be responsible for the flows and impact
    caused by their decisions pertaining to this
    """

    def __post_init__(self):
        self.setup = Add(flow=Inv, label='Setup')
        self.dismantle = -self.setup
        self.buy = Add(flow=Resource, label='Buy')
        self.sell = -self.buy

