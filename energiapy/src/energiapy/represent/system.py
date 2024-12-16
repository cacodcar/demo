# """System Model Block represents the Scenario through Components
# """

# from typing import Self

# from dataclasses import dataclass

# from ..components.flow.cash import Cash
# from ..components.use.land import Land
# from ..components.use.material import Material
# from ..components.flow.resource import Resource
# from ..components.operation.process import Process
# from ..components.operation.storage import Storage
# from ..components.operation.transit import Transit


# @dataclass
# class System:
#     """System is the representation of the Scenario through the use of Components

#     The methodology of commodification of the Scenario draws from the resource task network (RTN)

#     Read more about the RTN methodology in the following paper:

#         Barbosa-Póvoa, A. P. F. D., & Pantelides, C. C. (1997).
#         Design of multipurpose plants using the resource-task network unified framework.
#         Computers & chemical engineering, 21, S703-S708.

#     The Components that can be added to the System are:

#     Temporal:
#         - Scale

#     Spatial:
#         - Location
#         - Linkage

#     Commodities:
#         - Resource
#         - Emission
#         - Cash
#         - Land

#     Operations:
#         - Process
#         - Storage
#         - Transit

#     Scales and Locations are birthed internally

#     Storages birth Charging and Discharging Processes and ResourceStg
#     Transits birth Loading and Unloading Processes and ResourceTrn

#     Attributes:

#         name (str): name of the System, takes from Scenario

#     """

#     name: str = None

#     def __post_init__(self):

#         self.name = str(self.name)

#         # Program of the System
#         if self.name:
#             self.program = Prg(self.name)

#         else:
#             self.name = 'sys'
#             self.program = Prg()

#         # create empty lists to collect declared components
#         # commodities
#         self.emissions: list[Emission] = []
#         self.socials: list[Social] = []
#         self.cashes: list[Cash] = []
#         self.resources: list[Resource] = []
#         self.lands: list[Land] = []
#         # operations
#         self.processes: list[Process] = []
#         self.storages: list[Storage] = []
#         self.transits: list[Transit] = []

#     def __setattr__(self, name, component):

#         # Resources
#         if isinstance(component, Resource):
#             self.resources.append(component)

#         if isinstance(component, Land):
#             self.lands.append(component)

#         # if isinstance(component, Material):

#         # operations
#         if isinstance(component, Process):
#             self.processes.append(component)

#         if isinstance(component, Storage):
#             self.storages.append(component)

#         if isinstance(component, Transit):
#             self.transits.append(component)

#         super().__setattr__(name, component)

#     @property
#     def flows(self):
#         """Returns the Commodity Components of the System"""
#         return self.resources + self.emissions + self.cashes + self.lands

#     @property
#     def operations(self):
#         """Returns the Operations of the System"""
#         return self.processes + self.storages + self.transits

#     @property
#     def components(self):
#         """Returns all the Components of the System"""
#         return self.flows + self.operations

#     def __repr__(self):
#         return self.name

#     def __hash__(self):
#         return hash(self.name)

#     def __add__(self, other: Self) -> Self:
#         if isinstance(sys, System):
#             sys = System()
#             for i in self.components + other.components:
#                 setattr(sys, i.name, i)
#             return sys
#         return NotImplementedError
