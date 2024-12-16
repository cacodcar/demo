"""Impact - Environmental and Social"""

from ..components.impact.econ import Econ
from ..components.impact.environ import Environ
from ..components.impact.social import Social
from ..components.types.basic import BscCmp


class Impact(BscCmp):
    """The environmental and social impact of a system"""

    def __init__(self):

        self.environs: list[Environ] = []
        self.socials: list[Social] = []
        self.econs: list[Econ] = []

        BscCmp.__init__(self, 'All Impacts')

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
