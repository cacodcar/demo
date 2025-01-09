"""A Model"""

from dataclasses import dataclass
from itertools import product

from gana.block.program import Prg
from gana.sets.index import I

from ..components.commodity.misc import Cash, Land, Material
from ..components.commodity.resource import Resource
from ..components.game.player import Player
from ..components.impact.categories import Econ, Environ, Social
from ..components.operation.process import Process
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from ..components._core.tag import Name
from ..components._core.sample import Index
from .impact import Impact
from .space import Space
from .time import Time

0

from ..decisions.action import Action
from ..decisions.conseq import Conseq
from ..decisions.decision import Decision
from ..decisions.flow import Flow
from .design import Design


@dataclass
class Model:
    """An abstract representation of a system"""

    name: str = 'm'

    def __post_init__(self):

        self.players: list[Player] = []

        self.time = Time()
        self.space = Space()
        self.impact = Impact()
        self.design = Design()

        self.currencies: list[Cash] = []
        self.resources: list[Resource] = []
        self.lands: list[Land] = []
        self.materials: list[Material] = []
        self.processes: list[Process] = []
        self.added: list[str] = []

        # The base mathematical program
        self._program = Prg('Program(' + self.name + ')')

        # flag: True if component added
        self._upd = False

        for idxset in [
            'players',
            'scales',
            'locs',
            'links',
            'spaces',
            'currencies',
            'environs',
            'socials',
            'econs',
            'resources',
            'lands',
            'materials',
            'processes',
        ]:
            setattr(self._program, idxset, I(mutable=True))

        self.set_design()

    def __setattr__(self, name, value):

        if isinstance(value, (Name, Index)):
            value.name = name

            if isinstance(value, Index):
                value.model = self
                value.program = Prg(name)

            if hasattr(self, 'added'):
                if name in self.added:
                    if name not in ['_program']:
                        raise ValueError(f'{name} already defined')
                self.added.append(name)

        if isinstance(value, Player):
            self.players.append(value)
            self._program.players |= I(name)

        elif isinstance(value, Period):
            setattr(self.time, name, value)

        elif isinstance(value, Loc):
            setattr(self.space, name, value)
            self._program.locs |= I(name)
            self._program.spaces |= I(name)

        elif isinstance(value, Link):
            setattr(self.space, name, value)
            if value.bi:
                rev = value.rev()
                setattr(self, rev.name, rev)
            self._program.links |= I(name)
            self._program.spaces |= I(name)

        elif isinstance(value, Environ):
            setattr(self.impact, name, value)
            self._program.environs |= I(name)

        elif isinstance(value, Social):
            setattr(self.impact, name, value)
            self._program.socials |= I(name)

        elif isinstance(value, Econ):
            setattr(self.impact, name, value)
            self._program.econs |= I(name)

        elif isinstance(value, Cash):
            self.currencies.append(value)
            self._program.currencies |= I(name)

        elif isinstance(value, Resource):
            self.resources.append(value)
            self._program.resources |= I(name)

        elif isinstance(value, Land):
            self.lands.append(value)
            self._program.lands |= I(name)

        elif isinstance(value, Material):
            self.materials.append(value)
            self._program.materials |= I(name)

        elif isinstance(value, Process):
            self.processes.append(value)
            self._program.processes |= I(name)

        elif isinstance(value, Decision):
            setattr(self.design, name, value)

        super().__setattr__(name, value)

    @property
    def _(self):
        """gana program"""
        return self._program

    @property
    def horizon(self):
        """The horizon of the Model"""
        return self.time.horizon

    @property
    def network(self):
        """The network of the Model"""
        return self.space.network

    @property
    def actions(self):
        """The actions of the Model"""
        return self.design.actions

    @property
    def flows(self):
        """The flows of the Model"""
        return self.design.flows

    @property
    def conseqs(self):
        """The consequences of the Model"""
        return self.design.conseqs

    @property
    def decisions(self):
        """The decisions of the Model"""
        return self.design.decisions

    @property
    def program(self):
        """The program for the Model"""
        for cash in self.currencies:
            self._program += cash._program
        for environ in self.impact.environs:
            self._program += environ._program
        for social in self.impact.socials:
            self._program += social._program
        for econ in self.impact.econs:
            self._program += econ._program
        for resource in self.resources:
            self._program += resource._program
        for land in self.lands:
            self._program += land._program
        for material in self.materials:
            self._program += material._program
        for process in self.processes:
            self._program += process._program

        return self._program

    def pprint(self, descriptive: bool = False):
        """Pretty print the Model"""
        self.program.pprint(descriptive)

    def set_design(self):
        """Set the default for the Model"""

        # self.spend = Conseq(Econ, label='Economic Consequence')
        # self.earn = -self.spend

        # self.emit = Conseq(Environ, label='Environmental Consequence')
        # self.abate = -self.emit

        # self.detriment = Conseq(Social, label='Social Consequence')
        # self.benefit = -self.detriment

        # self.setup = Action(Process, label='Capacitate an Operation')
        # self.dismantle = -self.setup
        # self.use = Flow(Resource, label='Resource Flow caused by Operation Setup')
        # self.dispose = -self.use

        # self.operate = Action(Process, label='Operate an Operation')
        # self.consume = Flow(Resource, label='Resource consumed by Process operation')
        # self.produce = -self.consume

        # self.store = Action(Resource, label='Store a resource')
        # self.charge = Flow(Resource, label='Resource stored at Loc')
        # self.discharge = -self.charge

        # self.ship = Action(Resource, label='Ship a Resource')
        # self.send = Flow(Resource, label='Resource transported at Loc')
        # self.receive = -self.send

        # self.lose = Flow(Resource, label='Resource lost at Loc')

        # self.sell = Action(Player, label='Trade a Resource')
        # self.buy = -self.sell

        # for flow, cnsq in product(self.flows, self.conseqs):
        #     setattr(flow, cnsq.name, cnsq)

        # for attr in [self.setup, self.dismantle] + self.conseqs:
        #     setattr(self.setup, attr.name, attr)
        #     setattr(self.dismantle, attr.name, attr)

        # for action, motion, conseq in product(self.actions, self.flows, self.conseqs):

        #     setattr(action, motion.name, motion)
        #     setattr(action, conseq.name, conseq)

        #     setattr(motion, action.name, action)
        #     setattr(motion, conseq.name, conseq)

        #     setattr(conseq, action.name, action)
        #     setattr(conseq, motion.name, motion)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
