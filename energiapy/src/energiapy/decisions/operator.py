"""Opr"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from gana.sets.variable import V

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.function import F

    from ..components.space.linkage import Link
    from ..components.space.location import Loc
    from ..components.time.period import Period
    from ..components.types.modeling import ModCmp
    from .action import Act
    from .consequence import Cnsq
    from .flow import Flow


class Opr:
    """Oprs an action based on information (data/parameters) provided"""

    def __init__(
        self,
        decision: Act | Cnsq | Flow,
        space: Loc | Link,
        time: Period,
        cnsq: ModCmp = None,
        flow: ModCmp = None,
        act: ModCmp = None,
    ):
        self.decision = decision
        self.prg = decision.prg
        self.comp = decision.comp
        self.name = decision.name

        self.space = space
        self.time = time
        self.act = act
        self.flow = flow
        self.cnsq = cnsq


    def opr(
        self,
        other,
        cnsq: bool = True,
        flow: bool = True,
        act: bool = True,
        name: str = None,
    ):
        """Index"""
        idx = []

        if cnsq and self.cnsq:
            idx.append(self.cnsq.x)

        if flow and self.flow:
            idx.append(self.flow.x)

        if act and self.act:
            idx.append(self.act.x)

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
            setattr(self.prg, self.name, V(*idx, mutable=True))
            return getattr(self.prg, self.name)(*idx)

        if self.flow:
            setattr(self.flow.prg, name, V(*idx, mutable=True))
            return getattr(self.flow.prg, name)(*idx)

        if self.act:
            setattr(self.act.prg, name, V(*idx, mutable=True))
            return getattr(self.act.prg, name)(*idx)

    # def __add__(self, other: Self):
    #     return Opr(self.prg, self.opr + other.opr)

    # def __sub__(self, other: Self):
    #     return Opr(self.prg, self.opr - other.opr)

    # def __mul__(self, other: Self):
    #     return Opr(self.prg, self.opr * other.opr)

    # def __truediv__(self, other: Self):
    #     return Opr(self.prg, self.opr / other.opr)

    def __le__(self, other):
        setattr(
            self.prg, rf'ub_{self.name}_{self.prg.sets._nc}', self.opr(other) <= other
        )

    def __ge__(self, other):
        setattr(
            self.prg, rf'lb_{self.name}_{self.prg.sets._nc}', self.opr(other) >= other
        )

    def __eq__(self, other):

        if self.cnsq and self.flow and self.act:
            setattr(
                self.prg,
                rf'eq_{self.name}_{self.prg.sets._nc}',
                self.opr(other)
                == other
                * self.opr(
                    other, cnsq=False, name=f'{self.decision.act}_{self.decision.flow}'
                ),
            )

        elif self.cnsq and self.act and not self.flow:
            setattr(
                self.prg,
                rf'eq_{self.name}_{self.prg.sets._nc}',
                self.opr(other)
                == other * self.opr(other, cnsq=False, name=self.decision.act.name),
            )
        elif self.cnsq and self.flow and not self.act:
            setattr(
                self.prg,
                rf'eq_{self.name}_{self.prg.sets._nc}',
                self.opr(other)
                == other * self.opr(other, cnsq=False, name=self.decision.flow.name),
            )

        elif self.flow and self.act:
            setattr(
                self.prg,
                rf'eq_{self.name}_{self.prg.sets._nc}',
                self.opr(other)
                == other * self.opr(other, flow=False, name=self.decision.act.name),
            )

        else:
            setattr(
                self.prg,
                rf'eq_{self.name}_{self.prg.sets._nc}',
                self.opr(other) == other,
            )

    def __gt__(self, other):
        self >= other

    def __lt__(self, other):
        self <= other
