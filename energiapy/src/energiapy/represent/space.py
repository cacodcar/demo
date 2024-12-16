"""Space 
"""

from ..components.space.linkage import Link
from ..components.space.location import Loc
from ..components.types.basic import BscCmp


class Space(BscCmp):
    """Space"""

    def __init__(self):
        self.locs: list[Loc] = []
        self.sources: list[Loc] = []
        self.sinks: list[Loc] = []
        self.links: list[Link] = []
        BscCmp.__init__(self, 'Spatial representation of the system')

    def __setattr__(self, name, value):

        if isinstance(value, Loc):
            value.space = self
            self.locs.append(value)

        if isinstance(value, Link):
            value.space = self
            self.links.append(value)
            self.sources.append(value.source)
            self.sinks.append(value.sink)

        super().__setattr__(name, value)

    @property
    def network(self):
        """An encompassing region"""
        return max(self.locs, key=lambda x: x.depth())
