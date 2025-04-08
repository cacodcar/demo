"""Temporal Lag"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..core.tag import Name

if TYPE_CHECKING:
    from ...decisions.domain import Domain
    from .period import Period


@dataclass
class Lag(Name):
    """A number of temporal Periods"""

    of: Period = None
    periods: int | float = 1

    def __post_init__(self):
        self.name = f'-{self.periods}{self.of}'
        self.domains: list[Domain] = []
        # self.periods = self.of.periods
        # self.of = self.of.of

    @property
    def I(self):
        """Index set of scales"""
        return self.of.I - self.periods
