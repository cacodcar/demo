"""Materia used by Operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..commodity.resource import Trade, Use
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ..measure.basis import Basis


class Material(ModCmp, Trade, Use):
    """Materials are Resources, that are used to set up Operations"""

    def __init__(self, basis: Basis = None, label: str = None):
        self.basis = basis
        ModCmp.__init__(self, label)
        Trade.__init__(self)
        Use.__init__(self)
