"""Decision Space"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..decisions.action import Action
from ..decisions.conseq import Conseq
from ..decisions.decision import Decision
from ..decisions.flow import Flow
from .rep import Rep

if TYPE_CHECKING:
    from .model import Model
    from ..components._core.modeling import Component
    from ..components.spatial.location import Loc
    from ..components.spatial.linkage import Link
    from ..components.temporal.period import Period


class Design(Rep):
    """Polytope of the decision space"""

    def __init__(self):
        Rep.__init__(self)

        self.mdl: Model = None
        self.actions: list[Action] = []
        self.flows: list[Flow] = []
        self.conseqs: list[Conseq] = []

        self.hold_space: Loc | Link = None
        self.hold_time: Period = None
        self.hold_action: Component = None
        self.hold_flow: Component = None
        self.hold_conseq: Component = None

    @property
    def decisions(self):
        """All decisions"""
        return self.actions + self.flows + self.conseqs

    def __setattr__(self, name, value):

        if isinstance(value, Decision):
            value.name = name
            value.design = self

            if isinstance(value, Action):
                self.actions.append(value)
            elif isinstance(value, Flow):
                self.flows.append(value)
            elif isinstance(value, Conseq):
                self.conseqs.append(value)

        super().__setattr__(name, value)

    def reset(self, what: str = None):
        """Reset all holds"""

        if what:
            if what == 'space':
                self.hold_space = None
            elif what == 'time':
                self.hold_time = None
            elif what == 'action':
                self.hold_action = None
            elif what == 'flow':
                self.hold_flow = None
            elif what == 'conseq':
                self.hold_conseq = None
        else:
            self.reset('space')
            self.reset('time')
            self.reset('action')
            self.reset('flow')
            self.reset('conseq')
