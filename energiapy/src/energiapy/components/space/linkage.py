"""Linkage links Locations through Transits
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from ..types.scope import ScpCmp

if TYPE_CHECKING:
    from ...represent.space import Space
    from ..measure.basis import Basis


class Link(ScpCmp):
    """Linkage between two Locations"""

    def __init__(
        self,
        source,
        sink,
        dist: float = None,
        basis: Basis = None,
        bi: bool = False,
        label=None,
    ):

        self.source = source
        self.sink = sink
        self.dist = dist
        self.basis = basis
        self.space: Space = None
        self.bi = bi

        self.sib: Self = None

        ScpCmp.__init__(self, label)

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

        l = Link(
            source=self.sink,
            sink=self.source,
            dist=self.dist,
            basis=self.basis,
            label=label,
        )
        l.name = self.name + '_'
        l.sib = self
        self.sib = l
        return l
