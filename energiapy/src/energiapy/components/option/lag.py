"""Temporal Lag"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..time.period import Period


class Lag:
    """A number of temporal Periods"""

    def __init__(self, period: Period):
        self.name = f'-{period}'
        self.period = period
        self.periods = period.periods
        self.flow = period.flow

    @property
    def xset(self):
        """Index set of scales"""
        return self.flow.xset - self.periods

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
