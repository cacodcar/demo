"""Task"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._core.tag import Name


if TYPE_CHECKING:
    from ..commodity.resource import Resource
    from ..measure.basis import Basis


@dataclass
class Task(Name):
    """Process converts one Resource to another Resource"""

    def __post_init__(self):
        Name.__post_init__(self)
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

    def __eq__(self, other: Task):
        self.balance = {**self.balance, **other.balance}
        for res in self.balance.keys():
            setattr(res, self.name, self)
        return self

    def __add__(self, other: Task):
        if isinstance(other, Task):
            self.balance = {**self.balance, **other.balance}
            return self
        self.balance = {**self.balance, other: 1}
        return self

    def __sub__(self, other: Task):
        if isinstance(other, Task):
            self.balance = {
                **self.balance,
                **{res: -1 * par for res, par in other.balance.items()},
            }
            return self
        self.balance = {**self.balance, other: -1}
        return self
