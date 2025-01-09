"""Defined component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gana.sets.index import I
from gana.block.program import Prg

if TYPE_CHECKING:
    from ...modeling.model import Model


@dataclass
class Index:
    """A component with a mathematical program"""

    name: str = None
    label: str = None

    def __post_init__(self):
        # Model
        self.model: Model = None
        self.program: Prg = None
        self._program: Prg = Prg()
        self._indexed = False

    @property
    def index(self):
        """Index set"""
        if not self._indexed:
            setattr(self._program, self.name, I(self.name))
            self._indexed = True
        return getattr(self._program, self.name)

    @property
    def x(self):
        """gana index element (X)"""
        return getattr(self.program, self.name)

    @property
    def _(self):
        """gana index set (I)"""
        return self.index

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
