"""Scenario, is the core object 

    All Components defined as a scenario attribute.

    energiapy.components get added to the System Model Block
    Comps are the base for all components in energiapy, broadly categorized into
    Components the do not generate constraints and those that do.
    The former are further divided into -
          _Scope: Horizon, Network
          These create the spatiotemporal scope of the problem
    Scopes are further divided into -
          _Spatial: Location, Linkage
          _Temporal: Scale
          Locations and Scales are generated internally, Linkages are user-defined
    DefCmp components generate constraints which are added to the Program Model Block
    
    These include -
          _Commodity: Cash, Land, Resource, Material, Emission
          _Operation: Process, Storage, Transit
          _Analytical: Players
    The data provided as attributes is added to the Data Model Block
    provided data is converted into in internal formats: Constant, DataSet, Theta, M
    Theta - provided as tuple
    M - provided as True
    Constant - provided as float, int
    DataSet - provided as DataFrame
    Further any of these can be provided as a list to create an upper and lower bound for bounded variables
    
    The DataBlock is then added to the Program Model Block
    The Program Model Block is used to generate Parameters, Variables, Constraints, and Objectives
    
    The Matrix Model is just a matrix representation of the problem block
"""

from dataclasses import dataclass, field

from .._core._handy import _Dunders, _Print
from .._core._handy._words import reserved
from .._core.nirop.errors import ReservedWord
from ..components._base._component import ModCmp
from ..components._base._defined import DefCmp
from ..components.commodity.resource import ResourceStg, ResourceTrn
from ..components.operation._operation import _Operation
from ..components.operation.process import Process
from ..components.operation.storage import Storage
from ..components.operation.transit import Transit
from ..components.spatial.link import Linkage
from ..components.spatial.loc import Location
from ..components.temporal.period import Scale
from ._scenario._birth import _Birth
from ._scenario._default import _Default
from ._scenario._ok import _Ok
from ._scenario._update import _Update
from .model import Model
from .space import Network
from .time import Horizon


@dataclass
class Scenario(_Ok, _Default, _Birth, _Update, _Dunders, _Print):
    """
    A scenario for a considered system. It collects all the components of the model.

    Some default components can be created (def_ attributes):
        1. Network with no Locations or Linkages
        2. Horizon with only a root scale, i.e. the planning horizon (ph)
        3. Land with no bounds
        4. Cash with no bounds
        5. Players, viz. Consumer, Decision Maker, Market , Earth
        6. Emissions such as gwp, odp, etc.

    The strictness of checks can also be controlled (ok_ attribures).

    Attributes:
        name (str, optional): Name. Defaults to ':s:'.
        m (float): replaces 0 inputs with a small m (bearing this value). Default is None
        def_scope (bool): create default ScpCmp (Network, Horizon) Components. Default is False
        def_players (bool): create default (Players) Components. Default is False
        def_emissions (bool): create default (Emission) Components. Default is False
        def_cash (bool): create default (Cash) Components. Default is False
        def_land (bool): create default (Land) Components. Default is False
        default (bool): create default Components of all the above. Default is False
        ok_overwrite (bool): Allow overwriting of Components. Default is True
        ok_nobasis (bool): Allow Components without basis. Default is True
        ok_nolabel (bool): Allow Components without label. Default is True
        chill (bool): If False, disallow all the above. Default is True

    Examples:

        >>> from energiapy.components import Scenario
        >>> s = Scenario(name='Current')

    """

    name: str = field(default=':s:')

    def __post_init__(self):

        # Declare Model, contains system, program, data, matrix
        self.model = Model(name=self.name)
        _Ok.__post_init__(self)
        _Default.__post_init__(self)

        # set default values if self.default (inherited from _Default) is True
        self._default()

    def __setattr__(self, name, value):

        # All components are personlized with the attribute name provided
        # The Model [System, Program, Data, Matrix] is also added
        # This is a cursory step to check what is being added, also excludes name
        if isinstance(value, ModCmp):

            if name in reserved:
                raise ReservedWord(name)

            # Personalize the component
            value.personalize(name=name, model=self.model)

            # Check if ok to overwrite
            # Inherited from _Ok
            self.isok_overwrite(cmp=name)

            if isinstance(value, Scale):
                # horizon collects temporal Scales
                setattr(self.horizon, name, value)

            elif isinstance(value, Location):
                # network collects Locations
                setattr(self.network, name, value)

            elif isinstance(value, Linkage):
                setattr(self.network, name, value)
                self.birth_sib_linkage(linkage=value)
                # network collects Linkages too

            else:
                # set the component in the system
                setattr(self.system, name, value)

            # defined components generate constraints (ProgramBlock) which are added to the Program
            if isinstance(value, DefCmp):

                # Run some checks based on what is ok
                # Inherited from _Ok
                self.isok_nobasis(component=value)
                self.isok_nolabel(component=value)
                # All defined components have constraints
                # The data is handled first and made into internal formats and added to the Data Model
                # The Program Model is then generated using information from the Data Model
                self.update_model(name=name, component=value)

            # find where all the Operation is located
            # if nothing is provided, available throughout Network (all locations)
            if isinstance(value, _Operation):
                value.locate()

            # Operation are gotten from the System because at this point they are not set to the Scenario
            if isinstance(value, Process):
                process: Process = getattr(self.system, name)
                # make the conversion into a Conversion
                process.conversionize()
                self.locate_commodities(operation=process)

            if isinstance(value, Storage):
                storage: Storage = getattr(self.system, name)
                # make the inventory into Inventory
                storage.inventorize()
                # birth the Charging and Discharging processes
                # and the Storage Resource
                self.birth_bal_processes(operation=storage, res=ResourceStg())

            if isinstance(value, Transit):
                transit: Transit = getattr(self.system, name)
                # make the freight into Freight
                transit.freightize()
                # birth the Loading and Unloading processes
                # and the Transit Resource
                self.birth_bal_processes(operation=transit, res=ResourceTrn())

        super().__setattr__(name, value)

    @property
    def horizon(self):
        """Horizon of the Scenario"""
        return self.model.horizon

    @property
    def network(self):
        """Network of the Scenario"""
        return self.model.network

    @property
    def system(self):
        """System of the Scenario"""
        return self.model.system

    @property
    def program(self):
        """Program of the Scenario"""
        return self.model.program

    @property
    def taskmaster(self):
        """Chanakya of the Scenario"""
        return self.model.taskmaster

    @property
    def attr(self):
        """Attributes of the System"""
        return self.taskmaster

    @property
    def components(self):
        """All Components of the System"""
        return self.system.components

    @property
    def registrar(self):
        """Registrar of the Scenario"""
        return self.model.registrar

    def eqns(self, at_cmp=None, at_disp=None):
        """Prints all equations in the program
        Args:
            at_cmp (IsCmp, optional): Component to search for. Defaults to None.
            at_disp (IsIndex, optional): Idx to search for. Defaults to None.
        """
        for eqn in self.program.eqns(at_cmp=at_cmp, at_disp=at_disp):
            yield eqn
