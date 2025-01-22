"""Defined component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gana.sets.index import I

if TYPE_CHECKING:
    from ...modeling.model import Model


@dataclass
class Index:
    """A component with a mathematical program"""

    label: str = None

    def __post_init__(self):

        self.model: Model = None
        self.name: str = ''

    @property
    def program(self):
        """Mathematical program"""
        return self.model.program

    @property
    def index(self):
        """Index set"""
        return getattr(self.program, self.name)

    @property
    def I(self):
        """gana index set (I)"""
        index = I(self.name, mutable=True, tag=self.label)
        index.name = self.name
        return index

    def pprint(self, descriptive=False):
        """Pretty print the component"""
        return self.program.pprint(descriptive)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = Index.__repr__
        cls.__hash__ = Index.__hash__
