"""Class with functions to update:
    1. Components in the Scenario
    2. The Model Blocks 
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .....bin.program import Block
from ..._core.isalias.cmps.iscmp import IsUnq
from ..._core.isalias.cmps.isdfn import IsDfn, IsOpn
from ..time import Horizon


@dataclass
class _Update(ABC):
    """Has all the function needed to update the Scenario with Components and Model Blocks"""

    m: float = field(default=None)

    @property
    @abstractmethod
    def system(self):
        """System Model Block of the Scenario"""

    @property
    @abstractmethod
    def program(self):
        """Program Model Block of the Scenario"""

    # @property
    # @abstractmethod
    # def data(self):
    #     """Data Model Block of the Scenario"""

    @property
    @abstractmethod
    def taskmaster(self):
        """TaskMaster of the Scenario"""

    def cleanup(self, cmp: str):
        """Cleans up components which can have only one instance in the System
        Also the stuff they generate such as Scales (Horizon) and Locations (Network)

        Args:
            cmp (str): property in Scenario that stores Component 'horizon', 'network'
        """

        cmp: IsDfn = getattr(self, cmp)

        if cmp:
            if isinstance(cmp, Horizon):
                # remove scales if type Horizon
                for scale in cmp.scales:
                    delattr(self, scale.name)
                    delattr(self.system, scale.name)

            # remove the component from Scenario
            delattr(self, cmp.name)

            # remove the component from System
            delattr(self.system, cmp.name)

            # remove the component from Program Block
            if hasattr(self.program, cmp.name):
                delattr(self.program, cmp.name)

            # remove the component from Data Block
            if hasattr(self.data, cmp.name):
                delattr(self.data, cmp.name)

    def locate_commodities(self, operation: IsOpn):
        """Locates Commodities based on their participation in Operations

        Args:
            operation (IsOpn): _Operationn object
        """
        # commodities for Process come from conversion
        # for Storage from conersion_c and conversion_d
        # for Transit from freight
        for cmd in getattr(self.system, operation.name).commodities:
            if not cmd.is_located:
                cmd.locate()

    def handle_unique_cmp(self, cmp: str, component: IsUnq):
        """Handles components which can have only one instance in the System
        Args:
            cmp (str): 'cash', 'land', 'horizon', 'network'
            component(IsUnq): Component to be added

        """

        if getattr(self, f'_{cmp}'):
            # if there is an existing instance of the same type
            # remove it before adding the new one
            # also remove generated components such as scales and locations
            # also remove associated data and program if they exist
            self.cleanup(cmp)

        # set the component in the system
        setattr(self.system, cmp, component)

        # set the flag to True
        setattr(self, f'_{cmp}', True)

    def update_model(self, name: str, component: IsDfn):
        """Updates the Data and System Model with the components

        Args:
            name (str): name of component
            component (IsDfn): Component to be added
        """

        # Make the component inputs consistent
        # i.e. of the form - {Spatial[Location, Linkage, Network]: Temporal[Scale]: Mode[X]: Value}
        # Value can be numeric, DataFrame, True
        # or a tuple of numeric or DataFrame
        # or a list or numeric, DataFrame, True, or a tuple of numeric or DataFrame
        component.make_consistent(getattr(self, 'ok_inconsistent'))

        # make Small Blocks to be added to the larger Model Blocks
        # where all the model elements go
        programblock: Block = component.programblock
        programblock.m = self.m

        # Each DefCmp component has inputs which are categorized
        # check individual component parent classes _Operation, _Commodity (_Traded and _Used) for details
        for attr in component.inputs():
            if getattr(component, attr, False):
                # set the input as attribute in the DataBlock
                # This will make them into energiapy internal formats - Constant, DataSet, Theta, M
                programblock.write_constraints(
                    datum=getattr(component, attr), attr=attr
                )

        # The ProgramBlock is also added to the Program Model
        setattr(self.program, name, programblock)
