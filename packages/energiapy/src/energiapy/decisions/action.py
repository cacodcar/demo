"""Action(ion)"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from gana.sets.variable import V
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from .decision import Decision
from .operators import Opr

if TYPE_CHECKING:
    from .conseq import Conseq
    from .flow import Flow
    from ..components._core.modeling import Component


@dataclass
class Action(Decision):
    """Some action to be performed by a component
    that has a consequence (Conseq)
    or elicit a motion (Flow) that has a consequence (Conseq)
    """

    flow: Type[Component] = None
    domain: Type[Component] = None

    def __call__(self, *disp: Loc | Link | Period):

        space, time, flow, domain = (None for _ in range(4))
        for comp in disp:

            if isinstance(comp, (Loc, Link)):
                space = comp.x

            elif isinstance(comp, Period):
                time = comp.xset

            elif isinstance(comp, self.flow):
                flow = comp.x

            elif isinstance(comp, self.domain):
                domain = comp.x

        if not space:
            space = self.network.x

        if not time:
            time = self.horizon.xset

        if not flow:
            raise ValueError('Flow not defined')

        index = [i for i in [flow, domain, space, time] if i]

        setattr(self.program, self.name, V(*index, mutable=True))

        return Opr


@dataclass
class Add(Action):
    """Addition into domain"""


@dataclass
class Sub(Action):
    """Subtraction into domain"""


@dataclass
class Conv(Action):
    """Conversion into domain"""
