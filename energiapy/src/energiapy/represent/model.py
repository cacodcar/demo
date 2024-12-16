"""A Model"""

from dataclasses import dataclass

from gana.block.program import Prg
from gana.sets.index import I
from gana.sets.variable import V

from ..components.commodity.cash import Cash
from ..components.commodity.resource import Resource
from ..components.impact.econ import Econ
from ..components.impact.environ import Environ
from ..components.impact.social import Social
from ..components.operation.process import Process
from ..components.space.linkage import Link
from ..components.space.location import Loc
from ..components.time.period import Period
from ..components.types.basic import BscCmp
from ..components.types.defined import DefCmp
from ..components.use.land import Land
from ..components.use.material import Material
from .impact import Impact
from .space import Space
from .time import Time


@dataclass
class Model:
    """An abstract representation of a system"""

    name: str = 'm'

    def __post_init__(self):
        self.time = Time()
        self.space = Space()
        self.impact = Impact()

        self.currencies: list[Cash] = []
        self.resources: list[Resource] = []
        self.lands: list[Land] = []
        self.materials: list[Material] = []
        self.processes: list[Process] = []
        self.added: list[str] = []

        # The mathematical program
        self.prg = Prg('prg(' + self.name + ')')

        for idxset in [
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
            setattr(self.prg, idxset, I(mutable=True))

    def __setattr__(self, name, value):

        if isinstance(value, (BscCmp, DefCmp)):
            value.name = name

            if isinstance(value, DefCmp):
                value.mdl = self

            if hasattr(self, 'added'):
                if name in self.added:
                    if name not in ['prg']:
                        raise ValueError(f'{name} already defined')
                self.added.append(name)

        if isinstance(value, Period):
            setattr(self.time, name, value)

        elif isinstance(value, Loc):
            setattr(self.space, name, value)
            self.prg.locs |= I(name)
            self.prg.spaces |= I(name)

        elif isinstance(value, Link):
            setattr(self.space, name, value)
            if value.bi:
                rev = value.rev()
                setattr(self, rev.name, rev)
            self.prg.links |= I(name)
            self.prg.spaces |= I(name)

        elif isinstance(value, Environ):
            setattr(self.impact, name, value)
            self.prg.environs |= I(name)

        elif isinstance(value, Social):
            setattr(self.impact, name, value)
            self.prg.socials |= I(name)

        elif isinstance(value, Econ):
            setattr(self.impact, name, value)
            self.prg.econs |= I(name)

        elif isinstance(value, Cash):
            self.currencies.append(value)
            self.prg.currencies |= I(name)

        elif isinstance(value, Resource):
            self.resources.append(value)
            self.prg.resources |= I(name)

        elif isinstance(value, Land):
            self.lands.append(value)
            self.prg.lands |= I(name)

        elif isinstance(value, Material):
            self.materials.append(value)
            self.prg.materials |= I(name)

        elif isinstance(value, Process):
            self.processes.append(value)
            self.prg.processes |= I(name)

        super().__setattr__(name, value)

    @property
    def _(self):
        """gana program"""
        return self.prg

    @property
    def horizon(self):
        """The horizon of the Model"""
        return self.time.horizon

    @property
    def network(self):
        """The network of the Model"""
        return self.space.network

    @property
    def program(self):
        """The program for the Model"""
        for cash in self.currencies:
            self.prg += cash.prg
        for environ in self.impact.environs:
            self.prg += environ.prg
        for social in self.impact.socials:
            self.prg += social.prg
        for econ in self.impact.econs:
            self.prg += econ.prg
        for resource in self.resources:
            self.prg += resource.prg
        for land in self.lands:
            self.prg += land.prg
        for material in self.materials:
            self.prg += material.prg
        for process in self.processes:
            self.prg += process.prg

        return self.prg

    def pprint(self, descriptive: bool = False):
        """Pretty print the Model"""
        self.program.pprint(descriptive)

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
