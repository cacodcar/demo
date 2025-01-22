"""Modeling Component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .sample import Index

if TYPE_CHECKING:
    from ..measure.basis import Basis


@dataclass
class Component(Index):
    """A defined component with a mathematical program"""

    basis: Basis = None

    @property
    def design(self):
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

    def get(self, decision: str):
        """Give the decision"""
        # if not :
        #     setattr(self, decision, getattr(self.design, decision)(self))
        return getattr(self.design, decision)(self)
