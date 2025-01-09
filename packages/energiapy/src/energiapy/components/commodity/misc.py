from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from .resource import Resource
from ..operation.task import Task

from operator import is_

from ..impact.categories import Econ

if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..spatial.location import Loc


class Cash(Resource, Econ):
    """Same as Economic Impact (Econ)"""

    def __init__(self, *locs: Loc, label: str = None):

        Resource.__init__(self, *locs, label=label)
        Econ.__init__(self)

        # the locations, where this currency applies
        self.locs: tuple[Loc] = locs

        # also applies to all locations nested under the locations
        if locs:
            for loc in self.locs:
                for locin in loc.has:
                    if not locin in self.locs:
                        self.locs += (locin,)

            for loc in self.locs:
                # set the currency on the ensted locations as well
                loc.currency = self

        # a map of the exchange rates of currency
        # set using __eq__ method (==)
        self.exchange = Task()

    def __setattr__(self, name, value):
        if name == 'name' and value:
            self.exchange.name = f'exg({value})'

        super().__setattr__(name, value)

    def howmany(self, cash: Self):
        """Exchange rate basically"""

        if is_(cash, self):
            return 1
        if cash in self.balance:
            return self.balance[cash]
        raise ValueError(f'{cash} does not have an exchange rate set {self.name}')

    # TODO figure out exchange rates (again)
    # TODO using task
    def __eq__(self, other: Self | Cash | Task):

        if is_(other, self):
            return True

        if isinstance(other, Cash):
            other = 1 * other

        self.exchange += other

        # self.exchange.balance = {**other.balance, **self.exchange.balance}

        # for res in other.balance.keys():
        #     res.exchange.balance = {self: other.balance, **res.exchange.balance}
        return self

        # for c, r in cash.exchange.items():
        #     self.exchange[c] = rate / r
        #     c.exchange[self] = c.exchange[cash] / rate

        # self.exchange[cash] = rate
        # cash.exchange[self] = 1 / rate


@dataclass
class Emission(Resource):
    """Emission"""


@dataclass
class Material(Resource):
    """Materials are Resources, that are used to set up Operations"""


@dataclass
class Land(Resource):
    """Land used by Operations"""


@dataclass
class Package(Resource):
    """Package, discrete"""


@dataclass
class Human(Resource):
    """Human"""


@dataclass
class Mana(Resource):
    """Mana"""
