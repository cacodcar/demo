"""Impact - Environmental and Soc"""

from ..components.core.tag import Name
from ..components.impact.categories import Eco, Env, Soc


class Impact(Name):
    """The environmental and social impact of a system"""

    def __init__(self):

        self.environs: list[Env] = []
        self.socials: list[Soc] = []
        self.econs: list[Eco] = []

        Name.__init__(self, 'All Impacts')

    @property
    def indicators(self):
        """All indicators"""
        return self.environs + self.socials + self.econs

    def __setattr__(self, name, value):

        if isinstance(value, Env):
            value.impact = self
            self.environs.append(value)

        if isinstance(value, Soc):
            value.impact = self
            self.socials.append(value)

        if isinstance(value, Eco):
            value.impact = self
            self.econs.append(value)

        super().__setattr__(name, value)
