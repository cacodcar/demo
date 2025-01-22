"""Resource are: 
    1. converted by Processes
    2. stored by Storage
    3. transported by Transits
    4. lost by Storage and Transits
"""

from dataclasses import dataclass
from typing import Self

from ...decisions.default import Trade

# from ...decisions.flow import Flow
from .._core.modeling import Component
from ..operation.task import Task


@dataclass
class Resource(Component, Trade):
    """A resource, can be a material, chemical, energy, etc."""

    

    def __post_init__(self):

        Component.__post_init__(self)

        self.tasks: list[Task] = []
        # self.balance: dict[Task : int | float] = {}

        # self.produce = Flow(label='Amt of Resource operated upon')
        # self.consume = -self.produce

    @property
    def balance(self) -> dict[Task, int | float]:
        """Balance"""
        return {task: task.balance[self] for task in self.tasks}

    def __setattr__(self, name, value):

        if isinstance(value, Task):
            self.tasks.append(value)
            # self.balance = {value: value.balance[self], **self.balance}

        super().__setattr__(name, value)

    def __mul__(self, other: int | float) -> Task:
        task = Task()
        task.balance = {self: other}
        return task

    def __rmul__(self, other: int | float) -> Task:
        return self * other

    def __add__(self, other: Task) -> Task:
        task = Task()
        if isinstance(other, Resource):
            task.balance = {self: 1, other: 1}
            return task

        task.balance = {self: 1, **other.balance}
        return task

    def __neg__(self) -> Task:
        return self * -1

    def __sub__(self, other: Task | Self):
        if isinstance(other, Resource):
            return self + -1 * other
        if isinstance(other, Task):
            task = Task()
            task.balance = {
                self: 1,
                **{res: -1 * par for res, par in other.balance.items()},
            }
            return task

    def __truediv__(self, other: int | float):
        return self * (1 / other)

    def __rtruediv__(self, other: int | float):
        return self / other
