"""Component"""

from ...decisions.action import Act
from ...decisions.consequence import Cnsq
from ...decisions.flow import Flow
from .defined import DefCmp


class ModCmp(DefCmp):
    """A defined component with a mathematical program"""

    def __init__(self, label=None):

        DefCmp.__init__(self, label)

        self.actions: list[Act] = []
        self.consequences: list[Cnsq] = []
        self.flows: list[Flow] = []

    def __setattr__(self, name, value):

        if isinstance(value, Act):
            # if not value.comp:
            value.comp = self
            value.name = name
            self.actions.append(value)
            for elm in value.consequences + value.flows:
                elm.comp = self

            self.consequences += value.consequences
            self.flows += value.flows

        elif isinstance(value, Flow):
            value.comp = self
            value.naav = name
            self.flows.append(value)

            for cnsq in value.consequences:
                cnsq.comp = self
                self.consequences.append(value)

        elif isinstance(value, Cnsq):
            value.comp = self
            value.naav = name
            self.consequences.append(value)

        super().__setattr__(name, value)

    @property
    def network(self):
        """Circumscribing Loc"""
        return self.mdl.network

    @property
    def horizon(self):
        """Circumscribing Period"""
        return self.mdl.horizon

    @property
    def time(self):
        """Time"""
        return self.mdl.time

    @property
    def space(self):
        return self.mdl.space
