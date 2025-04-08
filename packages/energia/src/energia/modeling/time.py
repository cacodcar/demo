"""Time 
"""

from dataclasses import dataclass

from ..components.core.sample import Index
from ..components.temporal.period import Period


@dataclass
class Time(Index):
    """Temporal representation of a system"""

    def __post_init__(self):
        Index.__post_init__(self)
        self.periods: list[Period] = []

    def __setattr__(self, name, value):

        if isinstance(value, Period):
            value.time = self
            self.periods.append(value)

        super().__setattr__(name, value)

    @property
    def horizon(self) -> Period:
        """The sparsest scale is treated as the horizon"""
        return self.sparsest

    @property
    def densest(self) -> Period:
        """The densest period"""
        if self.periods:
            return min(self.periods, key=lambda x: x.periods)

    @property
    def sparsest(self) -> Period:
        """The sparsest period"""
        if self.periods:
            return max(self.periods, key=lambda x: x.periods)

    @property
    def tree(self) -> list[Period]:
        """Return the tree of periods"""
        hrz = self.horizon
        return {hrz.howmany(prd): prd for prd in self.periods}

    def find(self, size: int) -> Period:
        """Find the period that has the length"""
        return self.tree[size]
