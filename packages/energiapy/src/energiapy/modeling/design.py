"""Decision Space"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..components._core.tag import Name
from ..decisions.decision import Action, Conseq, Decision, Flow
from ..components.game.player import Player

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
