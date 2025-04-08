"""Time Period"""

from __future__ import annotations

from dataclasses import dataclass
from operator import is_
from typing import TYPE_CHECKING, Self

from gana.sets.index import I

from ..core.sample import Index
from .lag import Lag

if TYPE_CHECKING:
    from ...decisions.domain import Domain
    from ...modeling.time import Time


@dataclass
class Period(Index):
    """A discretization of Time"""

    periods: int | float = 1
    of: Self = None

    def __post_init__(self):

        self._periods = self.periods

        self._of = self.of

        if self.of and not self.of.isroot():
            self.periods = self.periods * self.of.periods
            self.of = self.of.of

        self.time: Time = None
        self._horizon: Self = None

        # can be overwritten by program
        self.name = f'{self._periods}{self._of}'

        self.domains: list[Domain] = []

    def isroot(self):
        """Is used to define another period?"""
        if not self.of:
            return True

    @property
    def I(self) -> I:
        """Index set of scale"""
        index = I(size=self.time.horizon.howmany(self), tag=self.label)
        index.name = self.name
        return index

    def howmany(self, period: Self):
        """How many periods make this period"""
        if period == self:
            return 1

        if period.isroot():
            if is_(period, self.of):
                return self.periods
            raise ValueError(f'{period} is not a period of {self.name}')

        if is_(period.of, self.of):
            p = self.periods / period.periods
            if p.is_integer():
                return int(p)
            return p

        if is_(self, period.of):
            return 1 / period.periods

        raise ValueError(f'{period} is not a period of {self.name}')

    def __mul__(self, times: int | float):
        if times < 0:
            if not self._of:
                return Lag(of=self, periods=-times)
            return Lag(of=self._of, periods=-times)
        return Period(periods=times, of=self)

    def __rmul__(self, other: int | float):
        return self * other

    def __call__(self, times):
        return Period(periods=times, of=self)

    def __neg__(self):
        return self * -1

    def __len__(self):
        return self.time.horizon.howmany(self)

    def __eq__(self, other: Self):
        return is_(self, other)
