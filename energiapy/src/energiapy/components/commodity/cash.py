"""Poishe, Money 
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..impact.econ import Econ

if TYPE_CHECKING:
    from ...represent.impact import Impact
    from ..space.location import Loc


class Cash(Econ):
    """Economic Impact"""

    def __init__(self, *locs: tuple[Loc], label: str = None):

        Econ.__init__(self, *locs, label=label)
