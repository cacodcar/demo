"""Time Period"""

from __future__ import annotations

from operator import is_
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from gana.sets.index import I

from .._core.sample import Index
from .lag import Lag

if TYPE_CHECKING:
    from ...modeling.time import Time


@dataclass
class Period(Index):
    """A discretization of Time"""

    periods: int | float = 1
    of: Self = None

    def __post_init__(self):

        if self.of and not self.of.isroot():
            self.periods = self.periods * self.of.periods
            self.of = self.of.of

        self.time: Time = None
        self._horizon: Self = None

        # can be overwritten by program
        self.name = f'{self.periods}{self.of}'

    def isroot(self):
        """Is used to define another period?"""
        if self.of:
            return False
        return True

    @property
    def xset(self) -> I:
        """Index set of scale"""
        if not self._indexed:
            setattr(self.program, self.name, I(size=self.time.horizon.howmany(self)))
            self._indexed = True
        return getattr(self.program, self.name)

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

    def __mul__(self, other: int | float):
        if isinstance(other, (int, float)):
            if other < 0:
                return -Period(-other, self)
            return Period(other, self)
        raise ValueError('Time Period can only be multiplied by a number')

    def __rmul__(self, other: int | float):
        return self * other

    def __neg__(self):
        return Lag(self)

    def __len__(self):
        return self.time.horizon.howmany(self)
