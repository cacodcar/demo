"""A Model"""

from dataclasses import dataclass
from itertools import product

from gana.block.program import Prg
from gana.sets.index import I
from gana.sets.variable import V

from ..components._core.sample import Index
from ..components._core.tag import Name
from ..components.commodity.misc import Cash, Land, Material
from ..components.commodity.resource import Resource
from ..components.game.player import Player
from ..components.impact.categories import Econ, Environ, Social
from ..components.operation.process import Process
from ..components.operation.storage import Storage
from ..components.operation.task import Task
from ..components.operation.transit import Transit
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from ..decisions.decision import Action, Conseq, Decision, Flow
from .design import Design
from .impact import Impact
from .space import Space
from .time import Time


@dataclass
class Model:
    """An abstract representation of a system"""

    name: str = 'm'
    default: bool = True

    def __post_init__(self):

        # The base mathematical program
        self.program = Prg('Program(' + self.name + ')')

        self.time = Time()
        self.space = Space()
        self.impact = Impact()
        self.design = Design(model=self)

        self.set_design()

        self.players: list[Player] = []
        self.currencies: list[Cash] = []
        self.resources: list[Resource] = []
        self.lands: list[Land] = []
        self.materials: list[Material] = []
        self.processes: list[Process] = []
        self.storages: list[Storage] = []
        self.added: list[str] = []

        self.tasks: list[Task] = []  # not added to program

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
            setattr(self.program, idxset, I(mutable=True))
        # if self.default:
        #     self.def_player = Player(label='Decision Maker')

    def __setattr__(self, name, value):

        if isinstance(value, Name):
            value.name = name

        if isinstance(value, Index):
            value.model = self
            value.name = name

            if hasattr(self, 'added'):
                if name in self.added:
                    if name not in ['program']:
                        raise ValueError(f'{name} already defined')
                self.added.append(name)

            if isinstance(value, Period):
                setattr(self.time, name, value)

            elif isinstance(value, Loc):
                setattr(self.space, name, value)
                self.program.locs |= I(name)
                self.program.spaces |= I(name)

            elif isinstance(value, Link):
                setattr(self.space, name, value)
                if value.bi:
                    rev = value.rev()
                    setattr(self, rev.name, rev)
                self.program.links |= I(name)
                self.program.spaces |= I(name)

            elif isinstance(value, Player):
                setattr(self.design, name, value)
                self.players.append(value)
                self.program.players |= I(name)

            elif isinstance(value, Environ):
                setattr(self.impact, name, value)
                self.program.environs |= I(name)

            elif isinstance(value, Social):
                setattr(self.impact, name, value)
                self.program.socials |= I(name)

            elif isinstance(value, Econ):
                setattr(self.impact, name, value)
                self.program.econs |= I(name)

            elif isinstance(value, Cash):
                self.currencies.append(value)
                self.program.currencies |= I(name)

            elif isinstance(value, Resource):
                # value.init('buy', 'sell')
                self.resources.append(value)
                self.program.resources |= I(name)

            elif isinstance(value, Land):
                self.lands.append(value)
                self.program.lands |= I(name)

            elif isinstance(value, Material):
                self.materials.append(value)
                self.program.materials |= I(name)

            elif isinstance(value, Process):
                self.processes.append(value)
                self.program.processes |= I(name)

        elif isinstance(value, Decision):
            setattr(self.design, name, value)
            setattr(self.program, name, V(mutable=True))

        elif isinstance(value, Task):
            # Cash can be declared through their exchange with other Cash
            if value.balance and isinstance(list(value.balance)[0], Cash):
                cash, task = Cash(), Task()
                cash.name = name
                task.name = list(value.balance)[0].name
                task.balance = {cash: list(value.balance.values())[0]}
                setattr(cash, task.name, task)
                setattr(self, name, cash)
                return
            else:
                setattr(self.design, name, value)
                self.tasks.append(value)

        super().__setattr__(name, value)

    @property
    def game(self):
        """Returns the game"""
        return self.design

    @property
    def _(self):
        """gana program"""
        return self.program

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
    def domains(self):
        """The domains of the Model"""
        return self.design.domains

    @property
    def _program(self):
        """The program for the Model"""
        for cash in self.currencies:
            self.program += cash.program
        for environ in self.impact.environs:
            self.program += environ.program
        for social in self.impact.socials:
            self.program += social.program
        for econ in self.impact.econs:
            self.program += econ.program
        for resource in self.resources:
            self.program += resource.program
        for land in self.lands:
            self.program += land.program
        for material in self.materials:
            self.program += material.program
        for process in self.processes:
            self.program += process.program

        return self.program

    def pprint(self, descriptive: bool = False):
        """Pretty print the Model"""
        self.program.pprint(descriptive)

    def set_design(self):
        """Set the default for the Model"""

        self.setup = Action(
            Operation=(Process, Storage, Transit), label='Capacitate Operation'
        )
        self.dismantle = -self.setup

        self.operate = Action(
            Operation=(Process, Storage, Transit), label='Operate Operation'
        )

        self.buy = Action(
            Resource=Resource, label='Exchange Resource with other player'
        )
        self.sell = -self.buy

        self.consume = Flow(
            Resource=Resource, label='Resource Flow caused by Operation'
        )

        self.produce = -self.consume

        self.earn = Conseq(Indicator=Econ, Resource=Resource, label='Transact')
        self.spend = -self.earn

        self.emit = Conseq(Indicator=Environ, Resource=Resource, label='Emit')
        self.abate = -self.emit

        self.detriment = Conseq(Indicator=Social, Resource=Resource, label='Detriment')
        self.benefit = -self.detriment

        self.export = Flow(Resource=Resource, label='Resource Flow between Locations')

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
