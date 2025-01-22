"""Decision"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, Type


from ..components.commodity.resource import Resource
from ..components.game.player import Player
from ..components.impact.indicator import Indicator
from ..components.operation.process import Process
from ..components.operation.storage import Storage
from ..components.operation.task import Task
from ..components.operation.process import Process
from ..components.operation.transit import Transit
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from .operators.bind import Bind

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components._core.sample import Index
    from ..modeling.design import Design
    from ..modeling.model import Model


@dataclass
class Decision:
    """Any kind of decision"""

    nn: bool = True
    Operation: Type[Process | Storage | Transit] = None
    Resource: Type[Resource] = None
    Indicator: Type[Indicator] = None
    label: str = None

    def __post_init__(self):
        # name of the decision
        self.design: Design = None
        self.name: str = ''
        self.neg: Self = None
        if self.label:
            if self.nn:
                self.label += ' [+]'
            else:
                self.label += ' [-]'
        self.domains: list[Loc | Link | Period] = []

    @property
    def model(self) -> Model:
        """Model"""
        return self.design.model

    @property
    def network(self):
        """Circumscribing Loc (Spatial Scale)"""
        return self.model.network

    @property
    def horizon(self):
        """Circumscribing Period (Temporal Scale)"""
        return self.model.horizon

    @property
    def time(self):
        """Time"""
        return self.model.time

    @property
    def space(self):
        """Space"""
        return self.model.space

    @property
    def program(self) -> Prg:
        """Mathematical Program"""
        return self.model.program

    @property
    def def_player(self) -> Player:
        """Player"""
        return self.model.def_player

    def __neg__(self):
        """Negative Consequence"""
        dscn = type(self)(
            nn=False,
            Operation=self.Operation,
            Resource=self.Resource,
            Indicator=self.Indicator,
        )
        dscn.neg, self.neg = self, dscn
        return dscn

    def __init_subclass__(cls):
        cls.__repr__ = Decision.__repr__
        cls.__hash__ = Decision.__hash__

    def __len__(self):
        return len(self.domains)

    def __call__(self, *index: Index):

        player, indicator, resource, task, process, operate, space, time = (
            None for _ in range(8)
        )
        timed, spaced = False, False

        for comp in index:

            if isinstance(comp, (Loc, Link)):
                if not comp == self.network:
                    space = comp
                    spaced = True
            elif isinstance(comp, Period):
                if not comp == self.horizon:
                    time = comp
                    timed = True

            elif self.Operation and isinstance(comp, self.Operation):
                operate = comp

            elif self.Indicator and isinstance(comp, self.Indicator):
                indicator = comp

            elif self.Resource and isinstance(comp, self.Resource):
                resource = comp

            elif isinstance(comp, Task):
                task = comp

            elif isinstance(comp, Process):
                process = comp

            elif isinstance(comp, Player):
                player = comp

            else:
                raise ValueError(f'{comp} not recognized as an index')

        index = [
            i
            for i in [player, indicator, resource, task, process, operate, space, time]
            if i
        ]

        return Bind(decision=self, index=index, timed=timed, spaced=spaced)

    # def opt(self):
    #     """Optimize"""
    #     var = getattr(self.prg, self.name)
    #     setattr(self.prg, f'min({self.name})', inf(sum(var)))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class Action(Decision):
    """Some action to be performed by a component
    that has a consequence (Conseq)
    or elicit a motion (Flow) that has a consequence (Conseq)
    """


@dataclass
class Flow(Decision):
    """Flow of a Resource"""


@dataclass
class Conseq(Decision):
    """Consequence of an action"""
