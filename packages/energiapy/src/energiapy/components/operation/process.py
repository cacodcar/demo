"""Process converts one Resource to another Resource
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._core.modeling import Component

from .task import Task

from ...decisions.default import Capacitate, Operate

if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..commodity.resource import Resource


@dataclass
class Process(Component, Capacitate, Operate):
    """Process converts one Resource to another Resource"""

    basis: Basis = None

    def __post_init__(self):
        self.base: Resource = None
        self.balance: dict[Resource : int | float] = {}

    def __call__(self, thing: Resource | Task):
        """Task is called with a Resource to be converted"""
        if isinstance(thing, Task):
            self.balance = {**self.balance, **thing.balance}
            self.base = list(self.balance)[0]
        else:
            self.base = thing
            self.balance = {self.base: 1, **self.balance}
        setattr(self.base, self.name, self)
        return self
