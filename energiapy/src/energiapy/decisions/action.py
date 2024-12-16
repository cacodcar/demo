"""Act(ion)"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from gana.sets.variable import V

from ..components.space.linkage import Link
from ..components.space.location import Loc
from ..components.time.period import Period
from .consequence import Cnsq
from .flow import Flow
from .operator import Opr

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components.types.modeling import ModCmp


class Act:
    """Some action to be performed by a component
    that has a consequence (Cnsq)
    or elicit a flow (Flow) that has a consequence (Cnsq)
    """

    def __init__(
        self, flowtypes: list[Type[ModCmp]] = None, cnsqtypes: list[Type[ModCmp]] = None
    ):
        # set by component (Component)
        self.comp: ModCmp = None
        self.name: str = ''

        # counter
        self.n = 0

        # negative action
        # set if using negation
        self.neg: Act = None

        self.flowtypes = flowtypes
        self.cnsqtypes = cnsqtypes

        # Actions can induce a flow of components
        self.flows: list[Flow] = []

        if flowtypes:
            self.hasflow = True
            for flow in flowtypes:
                for f in flow().flows:
                    setattr(self, f.name, f)

        else:
            self.hasflow = False

        # Consequences of actions can be provided directly
        self.consequences: list[Cnsq] = []

        if cnsqtypes:
            self.hascnsq = True
            for cnsq in cnsqtypes:
                for c in cnsq().consequences:
                    setattr(self, c.name, c)
        else:
            self.hascnsq = False

    @property
    def args(self):
        """Types"""
        return {'flowtypes': self.flowtypes, 'cnsqtypes': self.cnsqtypes}

    def __setattr__(self, name, value):

        if isinstance(value, Cnsq):
            value.act = self
            value.naav = name
            value.comp = self.comp
            self.consequences.append(value)

        elif isinstance(value, Flow):
            value.act = self
            value.naav = name
            value.comp = self.comp
            self.flows.append(value)

            for cnsq in value.consequences:
                cnsq.act = self
                cnsq.comp = self.comp

        super().__setattr__(name, value)

    @property
    def prg(self) -> Prg:
        """Return the program of the component"""
        return self.comp.prg

    def __neg__(self):
        act = Act(**self.args)
        act.neg, self.neg = self, act
        return act

    def __call__(self, *disp: Loc | Link | Period):

        (
            space,
            time,
        ) = (None for _ in range(2))

        for comp in disp:
            if isinstance(comp, (Loc, Link)):
                space = comp

            elif isinstance(comp, Period):
                time = comp

        return Opr(decision=self, space=space, time=time, act=self.comp)

        # setattr(self.prg, self.name, V(self.comp.x, loc, time, mutable=True))
        # return Opr(self.prg, getattr(self.prg, self.name)(self.comp.x, loc, time))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
