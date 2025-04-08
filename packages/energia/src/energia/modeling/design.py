"""Decision Space"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..components.core.tag import Name
from ..components.game.player import Player
from ..decisions.decision import Action, Conseq, Decision, Flow

if TYPE_CHECKING:
    from .model import Model


@dataclass
class Design(Name):
    """Polytope of the decision space"""

    model: Model = None

    def __post_init__(self):

        self.actions: list[Action] = []
        self.flows: list[Flow] = []
        self.conseqs: list[Conseq] = []
        self.players: list[Player] = []

    @property
    def decisions(self):
        """All decisions"""
        return self.actions + self.flows + self.conseqs

    @property
    def domains(self):
        """All domains"""
        return list(set(sum([d.domains for d in self.decisions], [])))

    @property
    def desdom(self):
        """{decision: domains}"""
        return {d: d.domains for d in self.decisions if d.domains}

    @property
    def domdes(self):
        """{domain: decisions}"""

        dict_ = {d: [] for d in self.domains}

        for dom in self.domains:
            for dec in self.desdom:
                if dom in self.desdom[dec]:
                    dict_[dom].append(dec)

        return dict_

    @property
    def domflows(self):
        """{domain: flows}"""

        dict_ = {
            dom: [d for d in des if isinstance(d, Flow)]
            for dom, des in self.domdes.items()
        }
        return {dom: flows for dom, flows in dict_.items() if flows}

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

        elif isinstance(value, Player):
            self.players.append(value)

        super().__setattr__(name, value)
