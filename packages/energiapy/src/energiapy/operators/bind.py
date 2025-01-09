"""Bind"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gana.sets.variable import V

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.function import F

    from ..components.spatial.linkage import Link
    from ..components.spatial.location import Loc
    from ..components.temporal.period import Period
    from ..components._core.modeling import Component
    from ..decisions.action import Action
    from ..decisions.conseq import Conseq
    from ..decisions.flow import Flow


class Bind:
    """Bind a decision to a provided parameter"""

    def __init__(
        self,
        decision: Action | Conseq | Flow,
        space: Loc | Link,
        time: Period,
        conseq: Component = None,
        motion: Component = None,
        action: Component = None,
    ):
        self.decision = decision
        self.program = decision.program
        self.comp = decision.comp
        self.name = decision.name

        self.space = space
        self.time = time
        self.action = action
        self.motion = motion
        self.conseq = conseq

    def opr(
        self,
        other,
        conseq: bool = True,
        motion: bool = True,
        action: bool = True,
        name: str = None,
    ):
        """Index"""
        idx = []

        if conseq and self.conseq:
            idx.append(self.conseq.x)

        if motion and self.motion:
            idx.append(self.motion.x)

        if action and self.action:
            idx.append(self.action.x)

        if self.space:
            idx.append(self.space.x)
        else:
            idx.append(self.comp.network.x)

        if self.time:
            idx.append(self.time.xset)
        else:
            if isinstance(other, list):
                idx.append(self.comp.time.find(len(other)).xset)
            else:
                idx.append(self.comp.horizon.xset)

        if not name:
            setattr(self.program, self.name, V(*idx, mutable=True))
            return getattr(self.program, self.name)(*idx)

        if self.motion:
            setattr(self.motion.program, name, V(*idx, mutable=True))
            return getattr(self.motion.program, name)(*idx)

        if self.action:
            setattr(self.action.program, name, V(*idx, mutable=True))
            return getattr(self.action.program, name)(*idx)

    def __le__(self, other):
        setattr(
            self.program,
            rf'ub_{self.name}_{self.program.sets._nc}',
            self.opr(other) <= other,
        )

    def __ge__(self, other):
        setattr(
            self.program,
            rf'lb_{self.name}_{self.program.sets._nc}',
            self.opr(other) >= other,
        )

    def __eq__(self, other):
        setattr(
            self.program,
            rf'eq_{self.name}_{self.program.sets._nc}',
            self.opr(other) == other,
        )
