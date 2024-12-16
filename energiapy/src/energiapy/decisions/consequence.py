"""Consequence (Cnsq)"""

from __future__ import annotations

from typing import TYPE_CHECKING

from gana.operations.composition import inf
from gana.sets.variable import V

from ..components.space.linkage import Link
from ..components.space.location import Loc
from ..components.time.period import Period
from .operator import Opr

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components.types.modeling import ModCmp
    from .action import Act
    from .flow import Flow


class Cnsq:
    """Consequence of performing an action (Act)
    or due to a FLow
    """

    def __init__(self):

        # set by action (Act)
        self.act: Act = None

        # what this is a consquence of?
        self.flow: Flow = None

        # set on which component
        self.comp: ModCmp = None
        # name of the consequence
        self.naav: str = ''

        # counter
        self.n = 0

        # negative consequence
        # set through negation
        self.neg: Cnsq = None

    @property
    def name(self) -> str:
        """Return the name of the consequence"""
        if self.act and self.flow:
            return f'{self.naav}_{self.flow}_{self.act}'
        else:
            if self.act:
                return f'{self.naav}_{self.act}'
            if self.flow:
                return f'{self.naav}_{self.flow}'
        return self.naav

    @property
    def prg(self) -> Prg:
        """Return the program of the component"""
        if self.comp:
            return self.comp.prg
        if self.flow:
            return self.flow.comp.prg
        return self.act.comp.prg

    def opt(self):
        """Optimize"""
        var = getattr(self.prg, self.name)
        setattr(self.prg, f'min({self.name})', inf(sum(var)))

    def __neg__(self):
        """Negative Consequence"""
        cnsq = Cnsq()
        cnsq.neg, self.neg = self, cnsq
        return cnsq

    def __call__(self, *disp: Loc | Link | Period | ModCmp):

        space, time, cnsq, flow, act = (None for _ in range(5))

        for comp in disp:

            if isinstance(comp, (Loc, Link)):
                space = comp

            elif isinstance(comp, Period):
                time = comp

            elif self.flow and isinstance(comp, tuple(self.flow.cnsqtypes)):
                cnsq = comp

            elif self.act and isinstance(comp, tuple(self.act.cnsqtypes)):
                cnsq = comp

            elif self.act and isinstance(comp, type(self.act.comp)):

                act = comp

            elif self.flow and isinstance(comp, type(self.flow.comp)):
                flow = comp

            if not flow and self.flow:
                flow = self.flow.comp

            if not act and self.act:
                act = self.act.comp

        return Opr(decision=self, space=space, time=time, cnsq=cnsq, flow=flow, act=act)

        # # consequences can be calculated
        # if self.flow:
        #     setattr(
        #         self.prg, self.name, V(dep, self.flow.comp.x, loc, time, mutable=True)
        #     )
        #     setattr(
        #         self.prg, self.flow.name, V(self.flow.comp.x, loc, time, mutable=True)
        #     )

        #     return Calc(
        #         self.prg,
        #         getattr(self.prg, self.name)(dep, self.flow.comp.x, loc, time),
        #         getattr(self.prg, self.flow.name)(self.flow.comp.x, loc, time),
        #     )

        # if self.act:
        #     setattr(
        #         self.prg, self.name, V(dep, self.act.comp.x, loc, time, mutable=True)
        #     )
        #     setattr(
        #         self.prg, self.act.name, V(self.act.comp.x, loc, time, mutable=True)
        #     )

        #     return Calc(
        #         self.prg,
        #         getattr(self.prg, self.name)(dep, self.act.comp.x, loc, time),
        #         getattr(self.prg, self.act.name)(self.act.comp.x, loc, time),
        #     )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
