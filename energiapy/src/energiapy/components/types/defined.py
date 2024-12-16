"""Defined component"""

from __future__ import annotations

from typing import TYPE_CHECKING

from gana.block.program import Prg
from gana.sets.index import I

if TYPE_CHECKING:
    from ...represent.model import Model


class DefCmp:
    """A component with a mathematical program"""

    def __init__(self, label=None):

        self.label = label

        # set by model
        self.name = ''

        # the program for each component is developed as we go
        self.prg = None
        self.mdl: Model = None
        self._indexed = False

    def __setattr__(self, name, value):

        if name == 'name' and value:
            self.prg = Prg(value)

        super().__setattr__(name, value)

    @property
    def index(self):
        """Index set"""
        if not self._indexed:
            setattr(self.prg, self.name, I(self.name))
            self._indexed = True
        return getattr(self.prg, self.name)

    @property
    def x(self):
        """gana index element (X)"""
        return getattr(self.mdl.prg, self.name)

    @property
    def _(self):
        """gana index set (I)"""
        return self.index

    @property
    def model(self):
        """The model for the Component"""
        return self.mdl

    @property
    def program(self):
        """The program for the Component"""
        return self.prg

    def pprint(self, descriptive=False):
        """Pretty print the component"""
        return self.prg.pprint(descriptive)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = DefCmp.__repr__
        cls.__hash__ = DefCmp.__hash__
