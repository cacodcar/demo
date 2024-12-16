"""Test to check where all components can be initialized 

This will inherently check if there are any abstract methods have not been implemented
"""

import pytest
from energiapy.src.energiapy.components.spatial.link import Linkage
from energiapy.src.energiapy.components.spatial.loc import Location
from src.energiapy.analytical.player import Player
from src.energiapy.component.flow.cash import Cash
from src.energiapy.component.flow.emission import Emission
from src.energiapy.component.flow.land import Land
from src.energiapy.component.flow.resource import Resource
from src.energiapy.component.operation.process import Process
from src.energiapy.component.operation.storage import Storage
from src.energiapy.component.operation.transit import Transit
from src.energiapy.component.temporal.period import Scale
from src.energiapy.elements.parameters.balances.conversion import Conversion
from src.energiapy.elements.parameters.balances.freight import Freight
from src.energiapy.elements.parameters.balances.inventory import Inventory
from src.energiapy.environ.horizon import Horizon
from src.energiapy.environ.network import Network


@pytest.fixture
def scn():
    s = Scenario()
    
    return Scenario()

def test_init(scn):
    



# TODO - set test to see uniqueness of birthed elements

# print(len(s.variables))
# print(len(set(s.variables)))
# print(len(set([v.name for v in s.variables])))
# print()
# print(len(s.parameters))
# print(len(set(s.parameters)))
# print(len(set([v.name for v in s.parameters])))
# print()
# print(len(s.constraints))
# print(len(set(s.constraints)))
# print(len(set([v.name for v in s.constraints])))
# print()
# print(len(s.dispositions))
# print(len(set(s.dispositions)))
# print(len(set([v.name for v in s.dispositions])))

# @pytest.fixture
# def scenario():
#     """Scenario"""
#     scn = Scenario()
#     scn.hrz = Horizon(birth=[1])
#     scn.ntw = Network(birth=['loca', 'locb'])
#     scn.lnk = Linkage(source=scn.loca, sink=scn.locb, bi=True)
#     scn.ply = Player()
#     scn.csh = Cash()
#     scn.lnd = Land()
#     scn.emn = Emission()
#     scn.mat = Material()
#     scn.res = Resource(
#         buy={scn.loca: {scn.t0: 1}},
#         sell={scn.locb: {scn.t1: 1}},
#         ship={scn.lnk: {scn.t0: 1}},
#         buy_price={scn.loca: {scn.t0: 1}},
#         sell_price={scn.locb: {scn.t1: 1}},
#         credit={scn.loca: {scn.t0: 1}},
#         penalty={scn.locb: {scn.t1: 1}},
#         buy_emission={scn.loca: {scn.t0: {scn.emn: 1}}},
#         sell_emission={scn.locb: {scn.t1: {scn.emn: 1}}},
#         loss_emission={scn.locb: {scn.t0: {scn.emn: 1}}},
#     )
#     scn.res_ = Resource()
#     scn.pro = Process(conversion={scn.res: {scn.res_: -1}})
#     scn.stg = Storage(inventory=scn.res)
#     scn.trn = Transit(freight=scn.res)
#     return scn


# def test_init(scenario):
#     """Test to check if all components can be initialized"""
#     # check if Model Blocks have been made
#     assert isinstance(scenario.model, Model)
#     assert isinstance(scenario.taskmaster, Chanakya)
#     assert isinstance(scenario.data, Data)
#     assert isinstance(scenario.matrix, Matrix)
#     assert isinstance(scenario.program, Program)
#     assert isinstance(scenario.system, System)

#     # check if Horizon has been made
#     # and being set as the horizon attribute
#     assert isinstance(scenario.hrz, Horizon)
#     assert hasattr(scenario, 'horizon') is True
#     assert isinstance(scenario.horizon, Horizon)
#     assert scenario.horizon == scenario.hrz
#     # check if scales are being set as attributes
#     # and collected in the scales attribute
#     assert hasattr(scenario, 't0') is True
#     assert isinstance(scenario.t0, Scale)
#     assert hasattr(scenario, 't1') is True
#     assert isinstance(scenario.t1, Scale)
#     assert scenario.scales == [scenario.t0, scenario.t1]
#     # check if network and locations are being set as attributes
#     assert isinstance(scenario.ntw, Network)
#     assert hasattr(scenario, 'network') is True
#     assert isinstance(scenario.network, Network)
#     assert hasattr(scenario, 'loca') is True
#     assert isinstance(scenario.loca, Location)
#     assert hasattr(scenario, 'locb') is True
#     assert isinstance(scenario.locb, Location)
#     # check if linkages are being set as attributes
#     # and the sibling linkage is being made
#     # and both are set to one direction
#     assert isinstance(scenario.lnk, Linkage)
#     assert scenario.lnk.source == scenario.loca
#     assert scenario.lnk.sink == scenario.locb
#     assert scenario.lnk.bi is False
#     assert hasattr(scenario, 'lnk_') is True
#     assert isinstance(scenario.lnk_, Linkage)
#     assert scenario.lnk_.source == scenario.locb
#     assert scenario.lnk_.sink == scenario.loca
#     assert scenario.lnk_.bi is False
#     # check out the commodities
#     # cash and land properties should be set as well
#     assert isinstance(scenario.ply, Player)
#     assert isinstance(scenario.csh, Cash)
#     assert hasattr(scenario, 'cash') is True
#     assert isinstance(scenario.cash, Cash)
#     assert isinstance(scenario.emn, Emission)
#     assert isinstance(scenario.lnd, Land)
#     assert hasattr(scenario, 'land') is True
#     assert isinstance(scenario.land, Land)
#     assert isinstance(scenario.mat, Material)
#     assert isinstance(scenario.res, Resource)
#     # check if process conversion is being made
#     assert isinstance(scenario.pro, Process)
#     assert isinstance(scenario.pro.conversion, Conversion)
#     # check if storage inverory is being made
#     assert isinstance(scenario.stg, Storage)
#     assert isinstance(scenario.stg.inventory, Inventory)
#     assert isinstance(scenario.stg.process_in, Process)
#     assert isinstance(scenario.stg.process_out, Process)
#     assert hasattr(scenario, 'stg_in') is True
#     assert hasattr(scenario, 'stg_out') is True
#     assert scenario.stg_in.conversion == scenario.stg.process_in.conversion
#     assert scenario.stg_out.conversion == scenario.stg.process_out.conversion
#     # check if transit freight is being made
#     # and set in transit
#     assert isinstance(scenario.trn, Transit)
#     assert isinstance(scenario.trn.freight, Freight)
#     assert isinstance(scenario.trn.process_in, Process)
#     assert isinstance(scenario.trn.process_out, Process)
#     assert hasattr(scenario, 'trn_in') is True
#     assert hasattr(scenario, 'trn_out') is True
#     assert scenario.trn_in.conversion == scenario.trn.process_in.conversion
#     assert scenario.trn_out.conversion == scenario.trn.process_out.conversion


# @pytest.fixture
# def spttmpinp(scenario):
#     """Datum"""
#     return Datum()


# @pytest.fixture
# def datablock(scenario):
#     """DataBlock"""
#     return DataBlock()


# @pytest.fixture
# def programblock(scenario):
#     """ProgramBlock"""
#     return ProgramBlock()


# def test_ind_init(spttmpinp, programblock, datablock):
#     assert isinstance(spttmpinp, Datum(dict_input={}))
#     assert isinstance(programblock, ProgramBlock)
#     assert isinstance(datablock, DataBlock)
