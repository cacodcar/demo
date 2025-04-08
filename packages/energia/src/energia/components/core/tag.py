"""Component"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...modeling.model import Model


@dataclass
class Name:
    """A component"""

    label: str = None

    def __post_init__(self):
        # set by the Model
        self.name = ''

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = Name.__repr__
        cls.__hash__ = Name.__hash__
