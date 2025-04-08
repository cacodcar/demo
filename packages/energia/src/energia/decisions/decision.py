"""Decision"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, Type
import matplotlib.pyplot as plt
from matplotlib import rc

from gana.sets.index import I

from ..components.commodity.resource import Resource
from ..components.game.player import Player
from ..components.impact.indicator import Indicator
from ..components.operation.process import Process
from ..components.operation.storage import Storage
from ..components.operation.transit import Transit
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.lag import Lag
from ..components.temporal.period import Period
from .balance import Bal
from .bind import Bind
from .domain import Domain

if TYPE_CHECKING:
    from gana.block.program import Prg
    from gana.sets.variable import V

    from ..components.core.sample import Index
    from ..modeling.design import Design
    from ..modeling.model import Model


@dataclass
class Decision:
    """Any kind of decision"""

    nn: bool = True
    Operation: Type[Process | Storage | Transit] = None
    Resource: Type[Resource] = None
    FResource: Type[Resource] = None
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
        self.indices: list[Loc | Link | Period] = []
        self.domains: list[Domain] = []
        # if a decision is bounded by another decision
        self.bound: Decision = None
        self.ispos = True

    @property
    def I(self):
        """gana index set (I)"""
        index = I(self.name, mutable=True, tag=self.label)
        index.name = self.name
        return index
    
    @property
    def V(self) -> V:
        """Variable"""
        return getattr(self.program, self.name)
    
    @property
    def index(self):
        """Index set"""
        return getattr(self.program, self.name)

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

    def sol(self):
        """Solution"""
        sol: V = getattr(self.program, self.name)
        return sol.sol()

    @property
    def def_player(self) -> Player:
        """Player"""
        return self.model.def_player

    def gettime(self, *index):
        """Finds the sparsest time scale in the domains"""
        ds = [i for i in self.indices if all([x in i for x in index])]
        t = [t for t in ds if isinstance(t, Period)]
        return t

    def __neg__(self):
        """Negative Consequence"""
        dscn = type(self)(
            nn=False,
            Operation=self.Operation,
            Resource=self.Resource,
            Indicator=self.Indicator,
            FResource=self.FResource,
        )
        dscn.neg, self.neg = self, dscn
        dscn.ispos = False
        return dscn

    def __init_subclass__(cls):
        cls.__repr__ = Decision.__repr__
        cls.__hash__ = Decision.__hash__

    def __len__(self):
        return len(self.domains)

    def __call__(self, *index: Index):

        (
            decision,
            player,
            indicator,
            resource,
            fresource,
            task,
            process,
            storage,
            transit,
            operate,
            space,
            time,
        ) = (None for _ in range(12))
        lag = False
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

            elif isinstance(comp, Lag):
                if not comp == self.horizon:
                    time = comp
                    timed = True
                    lag = True

            elif self.Operation and isinstance(comp, self.Operation):
                operate = comp

            elif self.Indicator and isinstance(comp, self.Indicator):
                indicator = comp

            elif self.Resource and isinstance(comp, self.Resource):
                resource = comp

            elif self.FResource and isinstance(comp, self.FResource):
                fresource = comp

            elif isinstance(comp, Bal):
                task = comp

            elif isinstance(comp, Process):
                process = comp

            elif isinstance(comp, Storage):
                storage = comp

            elif isinstance(comp, Transit):
                transit = comp

            elif isinstance(comp, Player):
                player = comp

            elif isinstance(comp, Bind):
                decision = comp

            else:
                raise ValueError(f'{self}:{comp} not recognized as an index')

        domain = Domain(
            decision=decision,
            player=player,
            indicator=indicator,
            resource=resource,
            fresource=fresource,
            task=task,
            process=process,
            storage=storage,
            transit=transit,
            operate=operate,
            space=space,
            time=time,
            lag=lag,
        )
        return Bind(decision=self, domain=domain, timed=timed, spaced=spaced)
    
    def plot(
        self,
        x: Index,
        y: tuple[Index] | Index,
        z: tuple[Index] | Index = None,
        font_size: float = 16,
        fig_size: tuple[float, float] = (12, 6),
        linewidth: float = 0.7,
        color: str = 'blue',
        grid_alpha: float = 0.3,
        usetex: bool = True,
    ):
        """Plot the decision"""
        if not isinstance(y, tuple):
            y = (y,)
        if not z:
            index = [i.I for i in y + (x,)]
        else:
            if not isinstance(z, tuple):
                z = (z,)

        if usetex:
            rc(
                'font',
                **{'family': 'serif', 'serif': ['Computer Modern'], 'size': font_size},
            )
            rc('text', usetex=usetex)
        else:
            rc('font', **{'size': font_size})

        fig, ax = plt.subplots(figsize=fig_size)
        if not z:
            ax.plot(
                [i.name for i in x.I._],
                self.V(*index).sol(True),
                linewidth=linewidth,
                color=color,
            )
        else:
            for z_ in z:
                index = [i.I for i in (z_,) + y + (x,)]
                ax.plot(
                    [i.name for i in x.I._],
                    self.V(*index).sol(True),
                    linewidth=linewidth,
                    label=z_.label if z_.label else z_.name,
                )

        label_ = [i.label if i.label else i.name for i in y]
        label_ = str(label_).replace("[", "").replace("]", "").replace("'", "")
        plt.title(f'{self.label} - {label_}')
        plt.ylabel("Values")
        plt.xlabel(f'{x.label or x.name}')
        plt.grid(alpha=grid_alpha)
        if z:
            plt.legend()
        if usetex:
            plt.rcdefaults()

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
