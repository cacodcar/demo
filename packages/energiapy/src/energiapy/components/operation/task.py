"""Task"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gana.sets.variable import V

from ...decisions.action import Action
from ..impact.categories import Econ
from ..impact.categories import Environ
from ..impact.categories import Social
from .._core.modeling import Component

if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..commodity.resource import Resource
    from ..spatial.location import Loc
    from ..temporal.period import Period


class Task(Component):
    """Process converts one Resource to another Resource"""

    def __init__(self, basis: Basis = None, label: str = None):

        Component.__init__(self, basis, label)

        self.base: Resource = None
        self.balance: dict[Resource : int | float] = {}

    def __call__(self, resource: Resource):
        self.base = resource
        self.balance = {self.base: 1, **self.balance}
        setattr(resource, self.name, self)
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

        # self.

        # setattr(
        #     self.prg,
        #     'produce',
        #     V(
        #         self.resource.x,
        #         self.x,
        #         self.network.x,
        #         self.horizon.xset,
        #         mutable=True,
        #     ),
        # )
        # exp = getattr(self.prg, 'produce')(
        #     self.resource.x, self.x, self.network.x, self.horizon.xset
        # )
        # if not isinstance(other.res, list):
        #     res_ = [other.res]
        #     mul_ = [other.mul]
        # else:
        #     res_ = other.res
        #     mul_ = other.mul
        # for res, par in zip(res_, mul_):
        #     if par > 0:
        #         setattr(
        #             self.prg,
        #             'produce',
        #             V(
        #                 res.x,
        #                 self.x,
        #                 self.network.x,
        #                 self.horizon.xset,
        #                 mutable=True,
        #             ),
        #         )
        #         exp += par * getattr(self.prg, 'produce')(
        #             res.x, self.x, self.network.x, self.horizon.xset
        #         )
        #     if par < 0:
        #         setattr(
        #             self.prg,
        #             'consume',
        #             V(
        #                 res.x,
        #                 self.x,
        #                 self.network.x,
        #                 self.horizon.xset,
        #                 mutable=True,
        #             ),
        #         )
        #         exp -= -par * getattr(self.prg, 'consume')(
        #             res.x, self.x, self.network.x, self.horizon.xset
        #         )

        # setattr(self.prg, self.name + '_conv', exp == 0)
