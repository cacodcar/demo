"""Flow"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from gana.sets.variable import V

from ..components.space.linkage import Link
from ..components.space.location import Loc
from ..components.time.period import Period
from .consequence import Cnsq
from .operator import Opr

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components.types.modeling import ModCmp
    from .action import Act


class Flow:
    """Flow elicited by an action (Act)"""

    def __init__(self, cnsqtypes: list[Type[ModCmp]] = None):

        # what this flow cause by?
        # set by action (Act)
        self.act: Act = None

        # set on which component
        self.comp: ModCmp = None
        # name of the consequence
        self.naav: str = ''

        # counter
        self.n = 0

        # negative flow
        self.neg: Flow = None

        self.cnsqtypes = cnsqtypes

        self.consequences: list[Cnsq] = []

        if cnsqtypes:
            self.hascnsq = True
            for cnsq in cnsqtypes:
                for c in cnsq().consequences:
                    setattr(self, c.name, c)
        else:
            self.hascnsq = False

    def hasact(self):
        """Flow of an action"""
        if self.act:
            return True

    def __setattr__(self, name, value):

        if isinstance(value, Cnsq):
            value.flow = self
            value.naav = name
            value.comp = self.comp
            self.consequences.append(value)

        super().__setattr__(name, value)

    @property
    def name(self) -> str:
        """Return the name of the consequence"""
        if self.act:
            return f'{self.naav}_{self.act}'
        return self.naav

    @property
    def prg(self) -> Prg:
        """Return the program of the component"""
        if self.comp:
            return self.comp.prg
        return self.act.comp.prg

    def __neg__(self):
        """Negative Consequence"""
        flow = Flow(self.cnsqtypes)
        flow.neg, self.neg = self, flow
        return flow

    def __call__(self, *disp: Loc | Link | Period | ModCmp):

        space, time, pending = (None for _ in range(3))
        for comp in disp:
            if isinstance(comp, (Loc | Link)):
                space = comp

            elif isinstance(comp, Period):
                time = comp

            else: 
                pending = comp 
            # elif self.act and isinstance(comp, type(self.act.comp)):
            #     act = comp

            # elif not self.act:
            #     print('asd')
            #     flow = comp
        
        if self.act: 
            act = self.act.comp
            flow = pending
        else: 
            act = pending
            flow = self.comp

        # if not flow:
        #     flow = self.comp

        return Opr(decision=self, space=space, time=time, flow=flow, act=act)

        # return Calc(
        #     self.prg,
        #     getattr(self.prg, self.name)(dep, self.act.comp.x, loc, time),
        #     getattr(self.prg, self.act.name)(self.act.comp.x, loc, time),
        # )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
