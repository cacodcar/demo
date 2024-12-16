"""Economic Impact"""

from __future__ import annotations

from operator import is_
from typing import TYPE_CHECKING, Self

from ...decisions.consequence import Cnsq
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ...represent.impact import Impact
    from ..space.location import Loc


class Econ(ModCmp):
    """Econ is a unit of currency that can be exchanged for other currencies"""

    def __init__(self, *locs: tuple[Loc], label: str = None):

        self.locs: tuple[Loc] = locs

        if locs:
            for loc in self.locs:
                for locin in loc.has:
                    if not locin in self.locs:
                        self.locs += (locin,)

            for l in self.locs:
                l.currency = self

        self.exchange: dict[Self, int | float] = {}

        ModCmp.__init__(self, label)

        self.earn = Cnsq()
        self.spend = -self.earn

        self.impact: Impact = None

    def howmany(self, cash: Self):
        """How many units of cash make this cash"""
        if is_(cash, self):
            return 1

        if cash in self.exchange:
            return self.exchange[cash]

        raise ValueError(f'{cash} is not a currency of {self.name}')

    def __mul__(self, other: int | float):
        return (self, other)

    def __rmul__(self, other: int | float):
        return self * other

    def __truediv__(self, other: int | float):
        return (self, 1 / other)

    def __eq__(self, other: tuple[Self, int | float]):

        if is_(other, self):
            return True

        if isinstance(other, tuple) and len(other) == 2:
            cash: Self = other[0]
            rate: int | float = other[1]

        if isinstance(cash, Econ) and isinstance(rate, (int, float)):

            for c, r in cash.exchange.items():
                self.exchange[c] = rate / r
                c.exchange[self] = c.exchange[cash] / rate

            self.exchange[cash] = rate
            cash.exchange[self] = 1 / rate
