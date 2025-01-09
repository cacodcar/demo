"""Linkage links Locations through Transits
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from .._core.sample import Index

if TYPE_CHECKING:
    from ...modeling.space import Space
    from ..measure.basis import Basis
    from .location import Loc


@dataclass
class Link(Index):
    """Linkage between two Locations"""

    source: Loc = None
    sink: Loc = None
    dist: float = None
    basis: Basis = None
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
            basis=self.basis,
            label=label,
        )
        _link.name = self.name + '_'
        _link.sib, self.sib = self, _link
        return _link

    def __eq__(self, dist: int | float):
        """Sets the distance of a linkage"""
        self.dist = dist
        return self
