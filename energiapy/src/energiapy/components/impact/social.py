"""Social Impact"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...decisions.consequence import Cnsq
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ...represent.impact import Impact


class Social(ModCmp):
    """Social Impact"""

    def __init__(self, label: str = None):

        self.impact: Impact = None

        ModCmp.__init__(self, label)

        self.benefit = Cnsq()
        self.detriment = -self.benefit
