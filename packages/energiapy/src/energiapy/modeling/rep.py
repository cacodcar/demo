"""Representation"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from .model import Model


class Rep:
    """A model representation"""

    def __init__(self):
        # set by the Model
        self.name = ''
        self.mdl: Model = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = Rep.__repr__
        cls.__hash__ = Rep.__hash__
