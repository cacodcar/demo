"""Emission, released based on some activity or operation 
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...decisions.consequence import Cnsq
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ...represent.impact import Impact


class Environ(ModCmp):
    """Environmental Impact"""

    def __init__(self, label: str = None):

        self.impact: Impact = None

        ModCmp.__init__(self, label)

        self.abate = Cnsq()
        self.emit = -self.abate
