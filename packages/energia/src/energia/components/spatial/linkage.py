"""Linkage links Locations through Transits
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from ..core.sample import Index
from ..measure.basis import Unit

if TYPE_CHECKING:
    from ...modeling.space import Space
    from .location import Loc


@dataclass
class Link(Index):
    """Linkage between two Locations"""

    source: Loc = None
    sink: Loc = None
    dist: float | Unit = None
    space: Space = None
    bi: bool = False
    sib: Self = None

    def rev(self):
        """Reversed Link"""
        if self.bi:
            self.bi = False
            return -self

    def __neg__(self):
        if self.label:
            label = self.label + '(-)'
            self.label = self.label + '(+)'
        else:
            label = None

        _link = Link(
            source=self.sink,
            sink=self.source,
            dist=self.dist,
            label=label,
        )
        _link.name = self.name + '_'
        _link.sib, self.sib = self, _link
        return _link

    def __eq__(self, dist: int | float):
        """Sets the distance of a linkage"""

        self.dist = dist

        self.model = self.source.model

        if not self.name:
            self.name = rf'{self.source.name}_{self.sink.name}'

        setattr(self.model, self.name, self)

        return self
