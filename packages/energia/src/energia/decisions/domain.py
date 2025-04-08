"""Domain"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..components.commodity.resource import Resource
    from ..components.game.player import Player
    from ..components.impact.indicator import Indicator
    from ..components.operation.process import Process
    from ..components.operation.storage import Storage
    from ..components.operation.transit import Transit
    from ..components.spatial.linkage import Link
    from ..components.spatial.location import Loc
    from ..components.temporal.period import Period
    from .balance import Bal
    from .decision import Decision


@dataclass
class Domain:
    """A domain"""

    decision: Decision = None
    player: Player = None
    indicator: Indicator = None
    resource: Resource = None
    fresource: Resource = None
    task: Bal = None
    process: Process = None
    storage: Storage = None
    transit: Transit = None
    operate: Process | Storage | Transit = None
    space: Loc | Link = None
    time: Period = None
    lag: bool = False

    def __post_init__(self):
        for i in self.index:
            i.domains.append(self)

    @property
    def index(self):
        """Index"""
        return [
            i
            for i in [
                self.decision,
                self.player,
                self.indicator,
                self.resource,
                self.fresource,
                self.task,
                self.process,
                self.storage,
                self.transit,
                self.operate,
                self.space,
                self.time,
            ]
            if i
        ]

    @property
    def _(self):
        """dict of indices"""
        return {
            'decision': self.decision,
            'player': self.player,
            'indicator': self.indicator,
            'resource': self.resource,
            'fresource': self.fresource,
            'task': self.task,
            'process': self.process,
            'storage': self.storage,
            'transit': self.transit,
            'operate': self.operate,
            'space': self.space,
            'time': self.time,
        }

    @property
    def Ilist(self):
        """List of I"""
        return [i.I for i in self.index]

    @property
    def name(self):
        """Name"""
        return f'{tuple(self.index)}'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == str(other)

    def __sub__(self, other):
        return [j for i, j in self._.items() if j and not i in other]
