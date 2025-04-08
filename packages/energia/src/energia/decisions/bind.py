"""Bind"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import TYPE_CHECKING, Self

from gana.operations.composition import inf
from gana.sets.function import F
from gana.sets.index import I
from gana.sets.variable import V

from ..components.core.tag import Name
from ..components.temporal.period import Period
from .calculate import Calc

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components.core.modeling import Component
    from ..modeling.model import Model
    from .decision import Decision
    from .domain import Domain


@dataclass
class Bind(Name):
    """Sets a bound on a decision Variable (V)"""

    decision: Decision = None
    domain: Domain = None
    timed: bool = None
    spaced: bool = None
    opr: F = None

    def __post_init__(self):
        self.name = self.decision.name
        if self.opr:
            self.domain = self.opr.index

        self.domains: list[Domain] = []

    @property
    def index(self):
        """Index"""
        return self.domain.index

    @property
    def I(self):
        """gana index set (I)"""
        index = I(self.name, mutable=True, tag=self.label)
        index.name = self.name
        return index

    @property
    def model(self) -> Model:
        """energia Model"""
        return self.decision.model

    @property
    def program(self) -> Prg:
        """gana Program"""
        return self.decision.program

    def V(self, parameters: int | list = None, length: int = None):
        """Sets the decision variable"""

        def time():
            if isinstance(parameters, list):
                self.domain.time = self.decision.time.find(len(parameters))
            elif isinstance(length, int):
                self.domain.time = self.decision.time.find(length)
            else:
                self.domain.time = self.decision.horizon

        def space():
            self.domain.space = self.decision.network

        if not self.spaced:
            space()

        if not self.timed:
            time()

        index = [i.I for i in self.domain.index]
        I = prod(index)

        if not I in self.decision.indices:
            # if self.domain.lag:
            #     index_ = index[:-1] + [self.domain.time.of.I]
            # else:
            #     index_ = index

            setattr(
                self.program,
                self.name,
                V(*index, mutable=True),
            )
            self.decision.indices.append(I)
            self.decision.domains.append(self.domain)

        return getattr(self.program, self.name)(*index)

    def Vb(self):
        """Bound Variable"""
        idx = [i for i in self.index if not isinstance(i, Period)]
        t = self.decision.bound.gettime(*idx)
        idx.extend(t)
        if len(t) > 0:
            return self.decision.bound(*idx).V(list(range(len(t))))
        else:
            return self.decision.bound(*idx).V(1)

    def opt(self):
        """Optimize"""
        var = getattr(self.program, self.name)
        self.model.stitch()
        setattr(self.program, f'min({self.name})', inf(sum(var)))
        self.program.opt()

    @property
    def F(self):
        """Function"""
        return self.V(1)

    def __le__(self, other):

        if self.decision.bound:
            vb = self.Vb()
            cons = self.V(other) <= other * vb

        else:
            cons = self.V(other) <= other

        setattr(
            self.program,
            rf'ub_{self.name}{self.program.sets._nc}',
            cons,
        )

    def __ge__(self, other):

        if self.decision.bound:
            vb = self.Vb()
            cons = self.V(other) >= other * vb

        else:
            cons = self.V(other) >= other

        setattr(
            self.program,
            rf'lb_{self.name}{self.program.sets._nc}',
            cons,
        )

    def __eq__(self, other):

        if self.decision.bound:
            vb = self.Vb()
            cons = self.V(other) == other * vb

        else:
            cons = self.V(other) == other

        setattr(
            self.program,
            rf'eq_{self.name}{self.program.sets._nc}',
            cons,
        )

    def __call__(self, *index):
        index = list(set(self.index + list(index)))
        return self.decision(*index)

    def __getitem__(self, dependent: Bind):
        if isinstance(dependent, int):
            return self.F(self.F.index[dependent])
        return Calc(calc=dependent(*self.index), decision=self(*self.index))

    def __gt__(self, other):
        self >= other

    def __lt__(self, other):
        self <= other

    def __add__(self, other: Self | FBind):
        if isinstance(other, (int, float)):
            return FBind(F=self.F + other, program=self.program)
        return FBind(F=self.F + other.F, program=self.program)

    def __radd__(self, other):
        if not other:
            return self

    def __sub__(self, other: Self | FBind):
        if isinstance(other, (int, float)):
            return FBind(F=self.F - other, program=self.program)
        return FBind(F=self.F - other.F, program=self.program)

    def __rsub__(self, other: int | float):
        return FBind(F=other - self.F, program=self.program)

    def __mul__(self, other: Self | FBind):
        return FBind(F=self.F * other.F, program=self.program)

    def __rmul__(self, other: int | float):
        return FBind(F=other * self.F, program=self.program)


class FBind:
    """Function Bind"""

    def __init__(self, F: F, program: Prg):
        self.program = program
        self.F = F

    def __add__(self, other: Self | Bind):
        if isinstance(other, (int, float)):
            return FBind(F=self.F + other, program=self.program)
        return FBind(F=self.F + other.F, program=self.program)

    def __radd__(self, other):
        if not other:
            return self

    def __sub__(self, other: Self | Bind):
        if isinstance(other, (int, float)):
            return FBind(F=self.F - other, program=self.program)
        return FBind(F=self.F - other.F, program=self.program)

    def __rsub__(self, other: int | float):
        return FBind(F=other - self.F, program=self.program)

    def __mul__(self, other: Self | Bind):
        return FBind(F=self.F * other.F, program=self.program)

    def __rmul__(self, other: int | float):
        return FBind(F=other * self.F, program=self.program)

    def __eq__(self, other):
        setattr(self.program, f'eq_{self.F.name}', self.F == other)

    def __le__(self, other):
        setattr(self.program, f'le_{self.F.name}', self.F <= other)

    def __ge__(self, other):
        setattr(self.program, f'ge_{self.F.name}', self.F >= other)
