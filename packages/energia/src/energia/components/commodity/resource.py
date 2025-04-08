"""Resource are: 
    1. converted by Processes
    2. stored by Storage
    3. transported by Transits
    4. lost by Storage and Transits
"""

from dataclasses import dataclass
from typing import Self

from ...decisions.balance import Bal
from ...decisions.default import Produce, Trade
# from ...decisions.flow import Flow
from ..core.modeling import Component


@dataclass
class Resource(Component, Trade, Produce):
    """A resource, can be a material, chemical, energy, etc."""

    def __post_init__(self):

        Component.__post_init__(self)
        self.stored: Resource = None
        self.tasks: list[Bal] = []
        # self.balance: dict[Bal : int | float] = {}

        # self.produce = Flow(label='Amt of Resource operated upon')
        # self.consume = -self.produce

    @property
    def balance(self) -> dict[Bal, int | float]:
        """Balance"""
        return {task: task.balance[self] for task in self.tasks}

    def __setattr__(self, name, value):

        if isinstance(value, Bal):
            self.tasks.append(value)
            # self.balance = {value: value.balance[self], **self.balance}

        super().__setattr__(name, value)

    def __mul__(self, other: int | float) -> Bal:
        task = Bal()
        task.balance = {self: other}
        return task

    def __rmul__(self, other: int | float) -> Bal:
        return self * other

    def __add__(self, other: Bal) -> Bal:
        task = Bal()
        if isinstance(other, Resource):
            task.balance = {self: 1, other: 1}
            return task

        task.balance = {self: 1, **other.balance}
        return task

    def __neg__(self) -> Bal:
        return self * -1

    def __sub__(self, other: Bal | Self):
        if isinstance(other, Resource):
            return self + -1 * other
        if isinstance(other, Bal):
            task = Bal()
            task.balance = {
                self: 1,
                **{res: -1 * par for res, par in other.balance.items()},
            }
            return task

    def __truediv__(self, other: int | float):
        return self * (1 / other)

    def __rtruediv__(self, other: int | float):
        return self / other
