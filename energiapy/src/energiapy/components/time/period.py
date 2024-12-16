"""Time Period"""

from __future__ import annotations

from operator import is_
from typing import TYPE_CHECKING, Self

from gana.sets.index import I

from ..option.lag import Lag
from ..types.scope import ScpCmp

if TYPE_CHECKING:
    from ...represent.time import Time


class Period(ScpCmp):
    """A discretization of Time"""

    def __init__(self, periods: int | float = 1, of: Self = None, label=None):

        if of and not of.isroot():
            periods = periods * of.periods
            of = of.flow

        self.periods = periods
        self.flow = of
        self.time: Time = None
        self._horizon: Self = None

        ScpCmp.__init__(self, label)

        # can be overwritten by program
        self.name = f'{periods}{of}'

    def isroot(self):
        """Is used to define another period?"""
        if self.flow:
            return False
        return True

    @property
    def xset(self) -> I:
        """Index set of scale"""
        if not self._indexed:
            setattr(self.prg, self.name, I(size=self.time.horizon.howmany(self)))
            self._indexed = True
        return getattr(self.prg, self.name)

    def howmany(self, period: Self):
        """How many periods make this period"""
        if period == self:
            return 1

        if period.isroot():
            if is_(period, self.flow):
                return self.periods
            raise ValueError(f'{period} is not a period of {self.name}')

        if is_(period.flow, self.flow):
            p = self.periods / period.periods
            if p.is_integer():
                return int(p)
            return p

        if is_(self, period.flow):
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
