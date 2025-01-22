"""Bind"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from gana.sets.function import F
from .calc import Calc
from gana.sets.variable import V

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.index import I

    from .decision import Decision


class Bind:
    """Sets a bound on a decision Variable (V)"""

    def __init__(
        self,
        decision: Decision,
        index: list[I] = None,
        opr: F = None,
    ):
        self.decision = decision
        self.name = decision.name
        self.program: Prg = decision.program

        if opr:
            index = opr.index
        else:
            opr = getattr(self.program, self.name)(*[i.I for i in index])

        self.index = index
        self.opr = opr

    def __le__(self, other):
        setattr(
            self.program,
            rf'ub_{self.name}',
            self.opr <= other,
        )

    def __ge__(self, other):
        setattr(
            self.program,
            rf'lb_{self.name}',
            self.opr >= other,
        )

    def __eq__(self, other):

        setattr(
            self.program,
            rf'eq_{self.name}',
            self.opr == other,
        )

    def __call__(self, *index):
        index = list(set(self.index + list(index)))
        return self.decision(*index)

    def __getitem__(self, dependent: Bind):

        setattr(
            self.program,
            dependent.name,
            V(*[i.I for i in self.index + dependent.index], mutable=True),
        )

        return Calc(dependent=dependent, decision=self.decision, index=self.index)

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
