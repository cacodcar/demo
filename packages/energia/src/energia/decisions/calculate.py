"""Calc"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.index import I

    from .bind import Bind
    from .decision import Decision


class Calc:
    """Calculate the value of a dependent variable (V*) based on a decision variable (V) value"""

    def __init__(
        self,
        calc: Bind,
        decision: Bind,
    ):
        self.decision = decision
        self.calc = calc(*decision.index)
        self.name = calc.name
        self.program: Prg = decision.program
        self.index = calc.index

    def __call__(self, *index):
        index = list(index) + self.index
        return Calc(calc=self.calc(*index), decision=self.decision)

    def __eq__(self, other):

        setattr(
            self.program,
            rf'calc_{self.name}{self.program.sets._nc}',
            self.calc(self.decision).V(other) == other * self.decision.V(other),
        )

    def __ge__(self, other):

        setattr(
            self.program,
            rf'LB_MS_{self.name}{self.program.sets._nc}',
            self.decision.V(other) >= other * self.calc.V(other),
        )

    def __le__(self, other):

        setattr(
            self.program,
            rf'UB_MS_{self.name}{self.program.sets._nc}',
            self.decision.V(other) <= other * self.calc.V(other),
        )
