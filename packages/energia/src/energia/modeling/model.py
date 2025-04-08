"""A Model"""

from dataclasses import dataclass

from gana.block.program import Prg
from gana.sets.index import I
from gana.sets.variable import V
from gana.operations.operators import sigma

from ..components.commodity.misc import Cash, Land, Material
from ..components.commodity.resource import Resource
from ..components.core.sample import Index
from ..components.core.tag import Name
from ..components.game.player import Player
from ..components.impact.categories import Eco, Env, Soc
from ..components.operation.process import Process
from ..components.operation.storage import Storage
from ..components.operation.transit import Transit
from ..components.spatial.linkage import Link
from ..components.spatial.location import Loc
from ..components.temporal.period import Period
from ..decisions.balance import Bal
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

        self.players: list[Player] = []
        self.currencies: list[Cash] = []
        self.resources: list[Resource] = []
        self.lands: list[Land] = []
        self.materials: list[Material] = []
        self.processes: list[Process] = []
        self.storages: list[Storage] = []
        self.transits: list[Transit] = []
        self.added: list[str] = []
        self.decisions: list[Decision] = []
        self.tasks: list[Bal] = []  # not added to program

        self.balance: dict[Process, dict[Resource, int | float | list]] = {}

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
            'storages',
            'transits',
            'decisions',
        ]:
            setattr(self.program, idxset, I(mutable=True))
        # if self.default:
        #     self.def_player = Player(label='Decision Maker')

        self.set_design()

    def __setattr__(self, name, value):

        if isinstance(value, Name):
            value.name = name

        if isinstance(value, Index):
            value.name = name
            value.model = self

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

            elif isinstance(value, Env):
                setattr(self.impact, name, value)
                self.program.environs |= I(name)

            elif isinstance(value, Soc):
                setattr(self.impact, name, value)
                self.program.socials |= I(name)

            elif isinstance(value, Eco):
                setattr(self.impact, name, value)
                self.program.econs |= I(name)

                if isinstance(value, Cash):
                    self.currencies.append(value)
                    self.program.currencies |= I(name)

            elif isinstance(value, Resource):
                # value.init('buy', 'sell')
                self.resources.append(value)
                self.program.resources |= I(name)

                if isinstance(value, Cash):
                    self.currencies.append(value)
                    self.program.currencies |= I(name)

                elif isinstance(value, Land):
                    self.lands.append(value)
                    self.program.lands |= I(name)

                elif isinstance(value, Material):
                    self.materials.append(value)
                    self.program.materials |= I(name)

            elif isinstance(value, Process):
                self.processes.append(value)
                self.program.processes |= I(name)

            elif isinstance(value, Storage):
                self.storages.append(value)
                self.program.storages |= I(name)

        elif isinstance(value, Decision):
            setattr(self.design, name, value)
            self.program.decisions |= I(name)
            # setattr(self.program, name, V(mutable=True))

        elif isinstance(value, Bal):
            # Cash can be declared through their exchange with other Cash
            if value.balance and isinstance(list(value.balance)[0], Cash):
                cash, task = Cash(), Bal()
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
    def commodities(self):
        """The commodities of the Model"""
        return self.resources + self.currencies + self.lands + self.materials

    @property
    def constraints(self):
        """The constraints of the Model"""
        return self.program.sets.constraint

    @property
    def variables(self):
        """The variables of the Model"""
        return self.program.sets.variable

    @property
    def parameters(self):
        """The parameters of the Model"""
        return self.program.sets.parameter

    @property
    def thetas(self):
        """The thetas of the Model"""
        return self.program.sets.theta

    # @property
    # def decisions(self):
    #     """The decisions of the Model"""
    #     return self.design.decisions

    @property
    def domains(self):
        """The domains of the Model"""
        return self.design.domains

    @property
    def domdes(self):
        """{domain: decisions}"""
        return self.design.domdes

    @property
    def desdom(self):
        """{decision: domains}"""
        return self.design.desdom

    @property
    def domflows(self):
        """{domain: flows}"""
        return self.design.domflows

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

        self.operate.bound = self.setup

        self.buy = Flow(Resource=Resource, label='Exchange Resource with other player')
        self.sell = -self.buy

        self.produce = Flow(
            Resource=Resource, label='Resource Flow caused by Operation'
        )

        self.consume = -self.produce

        self.inventory = Flow(
            Resource=Resource, Operation=Storage, label='Store Resource'
        )
        self.inventory.ispos = False

        self.earn = Flow(Resource=Cash, FResource=Resource, label='Transact')
        self.spend = -self.earn

        self.credit = Conseq(Indicator=Eco, Resource=Resource, label='Transact')
        self.debit = -self.credit

        self.emit = Conseq(Indicator=Env, Resource=(Resource, Material), label='Emit')
        self.abate = -self.emit

        self.detriment = Conseq(Indicator=Soc, Resource=Resource, label='Detriment')
        self.benefit = -self.detriment

        self.export = Flow(Resource=Resource, label='Resource Flow between Locations')

        self.dispose = Flow(
            Resource=(Land, Material),
            Operation=(Process, Storage, Transit),
            label='Utilize Resource',
        )

        self.use = -self.dispose

    def constraint_resource_balance(self):
        """Balance the Model"""
        dd = {r: {'domain': [], 'flows': [], 'time': []} for r in self.commodities}
        for d, f in self.domflows.items():
            dd[d.resource]['domain'].append(d - ['resource', 'time'])
            dd[d.resource]['time'].append(d.time)
            dd[d.resource]['flows'].extend(f)

        for resource, domflow in dd.items():
            give_, take_ = [], []
            if not isinstance(resource, Cash):
                # if inventory is being balanced
                # write constraint on densest temporal scale

                time = min(domflow['time'], key=lambda x: x.periods)

                # if self.inventory in domflow['flows']:
                #     time = self.time.densest

                # else:
                #     time = self.horizon
                # flows = []
                for dom, flow in zip(domflow['domain'], domflow['flows']):
                    # if not flow in flows:
                    # flows.append(flow)
                    if flow.ispos:
                        give_.append(flow(resource, *dom, time))

                    else:
                        take_.append(flow(resource, *dom, time))

                    if flow == self.inventory:
                        give_.append(self.inventory(resource, *dom, -time))
            if len(give_) > 0 and len(take_) > 0:
                sum(give_) - sum(take_) == 0

    def constraint_nameplate_prod(self):
        """Capacitate production"""

        # TODO : pull this into Domain
        def time(decision, process):
            times = [i.time for i in self.desdom[decision] if i.operate == process]
            t = min(times, key=lambda x: x.periods)
            return len(t)

        for prc in self.processes:
            setattr(
                self.program,
                f'cons_npc_{prc}',
                prc.operate.V(length=time(self.operate, prc))
                <= prc.setup.V(length=time(self.setup, prc)),
            )
            prc.constraints.append(f'cons_npc_{prc}')

    def constraint_nameplate_inv(self):
        """Capacitate storage"""

        def time(decision, process):
            times = [
                i.time
                for i in self.desdom[decision]
                if i.process == process or i.operate == process
            ]
            t = min(times, key=lambda x: x.periods)
            return len(t)

        for stg in self.storages:
            setattr(
                self.program,
                f'cons_npc_{stg}',
                stg.inventory(stg.stored).V(length=time(self.consume, stg.charge))
                <= stg.setup.V(length=time(self.setup, stg)),
            )
            stg.constraints.append(f'cons_npc_{stg}')

    def constraint_resource_flow(self):
        """Balance Resource Flow with Operational decisions"""

        def time(decision, resource, process):
            times = [
                i.time
                for i in self.desdom[decision]
                if i.resource == resource and i.process == process
            ]
            t = min(times, key=lambda x: x.periods)
            return len(t)

        for prc, bal in self.balance.items():
            for res, par in bal.items():
                if isinstance(par, (int | float)) and par < 0:
                    length = time(self.consume, res, prc)
                    setattr(
                        self.program,
                        f'cons_resflow_{prc}_{res}',
                        prc.operate.V(length=length)
                        == -par * self.consume(res, prc).V(length=length),
                    )

                elif isinstance(par, list) and par[0] < 0:
                    length = time(self.consume, res, prc)

                    setattr(
                        self.program,
                        f'cons_resflow_{prc}_{res}',
                        prc.operate.V(length=length)
                        == [-i for i in par] * self.consume(res, prc).V(length=length),
                    )

                else:
                    length = time(self.produce, res, prc)

                    setattr(
                        self.program,
                        f'cons_{prc}_{res}',
                        prc.operate.V(length=length)
                        == par * self.produce(res, prc).V(length=length),
                    )
                res.constraints.append(f'cons_resflow_{prc}_{res}')
                prc.constraints.append(f'cons_resflow_{prc}_{res}')

    def constraint_upscale(self):
        """Sum up to the horizon"""
        n = 0
        for des, dom in self.desdom.items():
            if not des == self.inventory:
                for d in dom:
                    if d.time != self.horizon:
                        d_t = d - 'time'
                        d_t = [i.I for i in d_t]
                        setattr(
                            self.program,
                            des.name,
                            V(*d_t, self.horizon.I, mutable=True),
                        )
                        setattr(self.program, des.name, V(*d_t, d.time.I, mutable=True))
                        v = getattr(self.program, des.name)
                        # print(v)
                        cons = sigma(v, d_t, d.time.I) == v(*d_t, self.horizon.I)

                        setattr(self.program, f'cons_time_balance{n}', cons)
                        n += 1
        n = 0
        for des, dom in self.desdom.items():
            idxs = []
            if not des == self.inventory:
                for d in dom:
                    if d.space != self.network:
                        d_s = d - 'space'
                        d_s = [i.I for i in d_s]
                        setattr(
                            self.program,
                            des.name,
                            V(*d_s[:-1], self.network.I, d_s[-1], mutable=True),
                        )
                        setattr(
                            self.program,
                            des.name,
                            V(*d_s[:-1], d.space.I, d_s[-1], mutable=True),
                        )
                        v = getattr(self.program, des.name)

                        idxs.append(d.Ilist)

                if len(idxs) > 0:
                    cons = sum(v(*idx) for idx in idxs) == v(
                        *idxs[0][:-2], self.network.I, idxs[0][-1]
                    )
                    # for n, idx in space_cons_dict.items():
                    #     cons = sum() == v(*idx[:-1], self.network.I, idx[-1])
                    setattr(self.program, f'cons_space_balance{n}', cons)

                    n += 1

    def stitch(self):
        """Make the model consistent"""
        # DONOT CHANGE ORDER
        # self.constraint_nameplate_inv()
        self.constraint_resource_balance()
        self.constraint_resource_flow()
        self.constraint_nameplate_prod()
        self.constraint_upscale()

    def sol(self):
        """Solution"""
        return self.program.sol()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
