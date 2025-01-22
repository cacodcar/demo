"""Bind"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from gana.sets.function import F
from gana.sets.variable import V
from .calc import Calc

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.index import I

    from ..decision import Decision
    from ...components._core.modeling import Component


class Bind:
    """Sets a bound on a decision Variable (V)"""

    def __init__(
        self,
        decision: Decision,
        timed: bool = None,
        spaced: bool = None,
        index: list[Component] = None,
        opr: F = None,
    ):
        self.decision = decision
        self.name = decision.name
        self.program: Prg = decision.program

        if opr:
            index = opr.index
        # else:
        #     opr = getattr(self.program, self.name)(*[i.I for i in index])

        self.index = index
        self.opr = opr
        self.timed = timed
        self.spaced = spaced

    def V(self, other: int | list):
        """Sets the decision variable"""

        index = self.index

        if not self.timed:
            if isinstance(other, list):
                index.append(self.decision.time.find(len(other)))

            else:
                index.append(self.decision.horizon)

        if not self.spaced:
            index.append(self.decision.network)

        setattr(
            self.program,
            self.name,
            V(*[i.I for i in index], mutable=True),
        )

        self.decision.domains.append(tuple(index))

        return getattr(self.program, self.name)(*[i.I for i in index])

    def __le__(self, other):

        setattr(
            self.program,
            rf'ub_{self.name}',
            self.V(other) <= other,
        )

    def __ge__(self, other):

        setattr(
            self.program,
            rf'lb_{self.name}',
            self.V(other) >= other,
        )

    def __eq__(self, other):

        setattr(
            self.program,
            rf'eq_{self.name}',
            self.V(other) == other,
        )

    def __call__(self, *index):
        index = list(set(self.index + list(index)))
        return self.decision(*index)

    def __getitem__(self, dependent: Bind):
        return Calc(calc=dependent(*self.index), decision=self(*self.index))

    def __gt__(self, other):
        self >= other

    def __lt__(self, other):
        self <= other

    def __add__(self, other: Self):
        return Bind(decision=self.decision, opr=self.opr + other.opr)

    def __sub__(self, other: Self):
        return Bind(decision=self.decision, opr=self.opr - other.opr)

    def __mul__(self, other: Self):
        return Bind(decision=self.decision, opr=self.opr * other.opr)
