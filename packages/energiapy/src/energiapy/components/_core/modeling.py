"""Modeling Component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...decisions.decision import Decision
from ...decisions.action import Action
from ...decisions.conseq import Conseq
from ...decisions.flow import Flow
from .sample import Index


if TYPE_CHECKING:
    from ..measure.basis import Basis


@dataclass
class Component(Index):
    """A defined component with a mathematical program"""

    basis: Basis = None

    def __post_init__(self):
        self.actions: list[Action] = []
        self.flows: list[Flow] = []
        self.conseqs: list[Conseq] = []

    def __setattr__(self, name, value):

        if isinstance(value, Decision):
            value.name = name
            value.comp = self

            if isinstance(value, Action):
                self.actions.append(value)

            elif isinstance(value, Flow):
                self.flows.append(value)

            elif isinstance(value, Conseq):
                self.conseqs.append(value)

        super().__setattr__(name, value)

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
