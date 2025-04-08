"""Space 
"""

from ..components.core.tag import Name
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc


class Space(Name):
    """Space"""

    def __init__(self):
        self.locs: list[Loc] = []
        self.sources: list[Loc] = []
        self.sinks: list[Loc] = []
        self.links: list[Link] = []
        Name.__init__(self, 'Spatial representation of the system')

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

        if not self.locs:
            ntw = Loc()
            ntw.name = 'ntw'
            return ntw

        if len(self.locs) == 1:
            return self.locs[0]
        
        # locs = [loc for loc in self.locs if not loc.isin]
        # ntw = Loc(*locs)
        # ntw.name = 'ntw'
        # return ntw

        return max(self.locs, key=lambda x: x.depth())
