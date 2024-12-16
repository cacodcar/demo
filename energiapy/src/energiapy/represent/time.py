"""Time 
"""

from ..components.time.period import Period
from ..components.types.basic import BscCmp


class Time(BscCmp):
    """Temporal representation of a system"""

    def __init__(self):
        self.periods: list[Period] = []

        BscCmp.__init__(self, 'Temporal representation of the system')

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
        return min(self.periods, key=lambda x: x.periods)

    @property
    def sparsest(self) -> Period:
        """The sparsest period"""
        return max(self.periods, key=lambda x: x.periods)

    @property
    def tree(self) -> list[Period]:
        """Return the tree of periods"""
        hrz = self.horizon
        return {hrz.howmany(prd): prd for prd in self.periods}

    def find(self, size: int):
        """Find the period that has the length"""
        return self.tree[size]
