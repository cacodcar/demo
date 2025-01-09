"""Decision"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period

from gana.sets.variable import V

if TYPE_CHECKING:
    from gana.block.program import Prg
    from ..components._core.modeling import Component
    from ..modeling.design import Design
    from ..modeling.model import Model


@dataclass
class Decision:
    """Any kind of decision"""

    label: str = None

    def __post_init__(self):
        # set by component (Component)
        self.comp: Component = None
        # name of the decision
        self.name: str = ''

        # negative decision
        # set through negation
        self.neg: Self = None

    def __setattr__(self, name, value):

        if name != 'neg' and isinstance(value, Decision):
            setattr(value, self.name, self)

        super().__setattr__(name, value)

    @property
    def model(self) -> Model:
        """Model"""
        return self.comp.model

    @property
    def design(self) -> Design:
        """Design"""
        return self.model.design

    @property
    def network(self):
        """Circumscribing Loc (Spatial Scale)"""
        return self.model.network

    @property
    def horizon(self):
        """Circumscribing Period (Temporal Scale)"""
        return self.model.horizon

    @property
    def time(self):
        """Time"""
        return self.model.time

    @property
    def space(self):
        """Space"""
        return self.model.space

    @property
    def program(self) -> Prg:
        """Mathematical Program"""
        return self.comp.program

    def __neg__(self):
        """Negative Consequence"""
        dscn = type(self)()
        dscn.neg, self.neg = self, dscn
        if self.label:
            self.label = '[+]' + self.label
            dscn.label = '[-]' + self.label
        return dscn

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    # def opt(self):
    #     """Optimize"""
    #     var = getattr(self.prg, self.name)
    #     setattr(self.prg, f'min({self.name})', inf(sum(var)))
