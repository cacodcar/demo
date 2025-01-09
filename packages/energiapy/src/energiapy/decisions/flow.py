"""Flow"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from .decision import Decision
from .operators import Opr

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components._core.modeling import Component
    from .action import Action
    from .conseq import Conseq


class Flow(Decision):
    """Flow induced by an action (Action)"""

    def __init__(self, label: str = None):

        Decision.__init__(self, label=label)
