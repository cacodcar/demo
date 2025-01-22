"""Storage - Stashes Resource to Withdraw Later
"""

from dataclasses import dataclass

# from ..._core.isalias.inps.isinp import IsBnd
# from ...elements.parameters.balances.inventory import Inventory
# from ..spatial.loc import Location
# from ._birther import _Birther


@dataclass
class Storage:
    """_summary_"""


# (
#     _Birther,
# ):
#     """Storage stores and withdraws Resources
#     There could be a dependent Resource

#     A ResourceStg is generate internally as the stored Resource
#     Charging and discharging Processes are also generated internally
#     Capacitate in this case is the amount of Resource that can be stored
#     Charging and discharging capacities can also be provided

#     Attributes:
#         capacity (IsBnd): bound on the capacity of the Operation
#         store: (IsBnd): bound by Capacitate. Reported by operate as well.
#         use (IsBnd): bound on amount of Land or Material used by Process
#         setup_use (IsExt): Land or Material setup_use per unit capacity
#         capex (IsInc): capital expense per Capacitate
#         opex (IsInc): operational expense based on Operation
#         use_emission (IsExt): emission due to land or Material use
#         setup_emission (IsExt): emission due to construction activity
#         inventory: (IsBlc): balance needed for storage. can just be a Resource as well
#         freight_loss: (IsExt): loss of resource in storage
#         capacity_c (IsBnd): bounds for capacity of generated charging Process
#         capacity_d (IsBnd): bounds for capacity of generated discharging Process
#         locations (list[Location]): Locations where the Storage is located
#         basis (str): basis of the component
#         citation (dict): citation of the component
#         block (str): block of the component
#         introduce (str): index in scale when the component is introduced
#         retire (str): index in scale when the component is retired
#         label (str): label of the component
#     """

#     inventory: dict | Inventory = field(default_factory=dict)
#     locations: list[Location] = field(default_factory=list)
#     setup_in: IsBnd = field(default=None)
#     setup_out: IsBnd = field(default=None)

#     def __post_init__(self):
#         _Birther.__post_init__(self)

#     @property
#     def balance(self):
#         """Balance of the Storage"""
#         return self.inventory

#     @staticmethod
#     def _at():
#         """Spatial attributes"""
#         return 'locations'

#     def inventorize(self):
#         """Makes the inventory"""
#         if not isinstance(self.inventory, Inventory):
#             self.inventory = Inventory(inventory=self.inventory, storage=self)
#             self._balanced = True
