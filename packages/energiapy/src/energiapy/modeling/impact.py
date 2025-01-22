"""Impact - Environmental and Social"""

from ..components._core.tag import Name
from ..components.impact.categories import Econ, Environ, Social


class Impact(Name):
    """The environmental and social impact of a system"""

    def __init__(self):

        self.environs: list[Environ] = []
        self.socials: list[Social] = []
        self.econs: list[Econ] = []

        Name.__init__(self, 'All Impacts')

    @property
    def indicators(self):
        """All indicators"""
        return self.environs + self.socials + self.econs

    def __setattr__(self, name, value):

        if isinstance(value, Environ):
            value.impact = self
            self.environs.append(value)

        if isinstance(value, Social):
            value.impact = self
            self.socials.append(value)

        if isinstance(value, Econ):
            value.impact = self
            self.econs.append(value)

        super().__setattr__(name, value)
