"""Opr"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from gana.sets.variable import V

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.function import F

    from ..components.spatial.linkage import Link
    from ..components.spatial.location import Loc
    from ..components.temporal.period import Period
    from ..components._core.modeling import Component
    from .action import Action
    from .conseq import Conseq
    from .flow import Flow


# class Binder:
#     """Binds a decision to a parameter set"""

#     def __init__(
#             self,
#             decision: Action | Conseq | Flow,
#             space: Loc | Link,
#             time: Period,
#             conseq: Component = None,
#             flow: Component = None,
#             action: Component = None,
#                  ):


class Opr:
    """Oprs an action based on information (data/parameters) provided"""

    def __init__(
        self,
        decision: Action | Conseq | Flow,
        space: Loc | Link,
        time: Period,
        conseq: Component = None,
        flow: Component = None,
        action: Component = None,
    ):
        self.decision = decision

        self.program = decision.prorgram
        self.comp = decision.comp
        self.name = decision.name

        self.space = space
        self.time = time
        self.action = action
        self.flow = flow
        self.conseq = conseq

    def opr(
        self,
        other,
        conseq: bool = True,
        flow: bool = True,
        action: bool = True,
        name: str = None,
    ):
        """Index"""
        idx = []

        if conseq and self.conseq:
            idx.append(self.conseq.x)

        if flow and self.flow:
            idx.append(self.flow.x)

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

        if self.flow:
            setattr(self.flow.program, name, V(*idx, mutable=True))
            return getattr(self.flow.program, name)(*idx)

        if self.action:
            setattr(self.action.program, name, V(*idx, mutable=True))
            return getattr(self.action.program, name)(*idx)

    def __le__(self, other):
        setattr(
            self.program, rf'ub_{self.name}_{self.program.sets._nc}', self.opr(other) <= other
        )

    def __ge__(self, other):
        setattr(
            self.program, rf'lb_{self.name}_{self.program.sets._nc}', self.opr(other) >= other
        )

    def __eq__(self, other):
        setattr(
            self.program, rf'eq_{self.name}_{self.program.sets._nc}', self.opr(other) == other
        )

        # if self.conseq and self.flow and self.action:
        #     setattr(
        #         self.program,
        #         rf'eq_{self.name}_{self.program.sets._nc}',
        #         self.opr(other)
        #         == other
        #         * self.opr(
        #             other,
        #             conseq=False,
        #             name=f'{self.decision.action}_{self.decision.flow}',
        #         ),
        #     )

        # elif self.conseq and self.action and not self.flow:
        #     setattr(
        #         self.program,
        #         rf'eq_{self.name}_{self.program.sets._nc}',
        #         self.opr(other)
        #         == other
        #         * self.opr(other, conseq=False, name=self.decision.action.name),
        #     )
        # elif self.conseq and self.flow and not self.action:
        #     setattr(
        #         self.program,
        #         rf'eq_{self.name}_{self.program.sets._nc}',
        #         self.opr(other)
        #         == other
        #         * self.opr(other, conseq=False, name=self.decision.flow.name),
        #     )

        # elif self.flow and self.action:
        #     setattr(
        #         self.program,
        #         rf'eq_{self.name}_{self.program.sets._nc}',
        #         self.opr(other)
        #         == other
        #         * self.opr(other, flow=False, name=self.decision.action.name),
        #     )

        # else:

    def __gt__(self, other):
        self >= other

    def __lt__(self, other):
        self <= other

    # def __add__(self, other: Self):
    #     return Opr(self.program, self.opr + other.opr)

    # def __sub__(self, other: Self):
    #     return Opr(self.program, self.opr - other.opr)

    # def __mul__(self, other: Self):
    #     return Opr(self.program, self.opr * other.opr)

    # def __truediv__(self, other: Self):
    #     return Opr(self.program, self.opr / other.opr)
