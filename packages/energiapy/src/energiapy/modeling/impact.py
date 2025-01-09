"""Impact - Environmental and Social"""

from ..components.impact.categories import Econ
from ..components.impact.categories import Environ
from ..components.impact.categories import Social
from ..components._core.tag import Name


class Impact(Name):
    """The environmental and social impact of a system"""

    def __init__(self):

        self.environs: list[Environ] = []
        self.socials: list[Social] = []
        self.econs: list[Econ] = []

        Name.__init__(self, 'All Impacts')

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
