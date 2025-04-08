"""Defined component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gana.sets.index import I

if TYPE_CHECKING:
    from ...decisions.domain import Domain
    from ...modeling.model import Model


@dataclass
class Index:
    """A component with a mathematical program"""

    label: str = None

    def __post_init__(self):

        self.model: Model = None
        self.name: str = ''
        self._I = None
        self.constraints: list[str] = []
        self.domains: list[Domain] = []

    @property
    def program(self):
        """Mathematical program"""
        return self.model.program

    @property
    def Idx(self):
        """gana index element (Idx)"""
        return getattr(self.program, self.name)

    @property
    def I(self):
        """gana index set (I)"""
        if not self._I:
            _I = I(self.name, mutable=True, tag=self.label)
            _I.name = self.name
            self._I = _I
        return self._I

    @property
    def cons(self):
        """Constraints"""
        return [getattr(self.program, c) for c in self.constraints]

    def pprint(self, descriptive=False):
        """Pretty print the component"""
        for c in self.cons:
            c.pprint(descriptive)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = Index.__repr__
        cls.__hash__ = Index.__hash__
