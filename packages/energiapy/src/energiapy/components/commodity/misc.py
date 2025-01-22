from __future__ import annotations

from dataclasses import dataclass
from operator import is_
from typing import TYPE_CHECKING, Self

# from ..operation.task import Task
from ...decisions.default import Transact
from ..impact.categories import Econ
from .resource import Resource

if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..spatial.location import Loc


class Cash(Resource, Econ, Transact):
    """Same as Economic Impact (Econ)"""

    def __init__(self, *locs: Loc, label: str = None):

        Resource.__init__(self, label=label)
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

    def howmany(self, cash: Self):
        """Exchange rate basically"""

        if is_(cash, self):
            return 1
        if cash in self.balance:
            return self.balance[cash]
        # find a common currency
        if list(self.balance)[0] == list(cash.balance)[0]:
            return (
                self.balance[list(self.balance)[0]]
                / cash.balance[list(cash.balance)[0]]
            )
        raise ValueError(f'{cash} does not have an exchange rate set {self.name}')


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
