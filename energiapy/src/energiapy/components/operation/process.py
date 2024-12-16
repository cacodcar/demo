"""Process converts one Resource to another Resource
"""

# """Process converts one Resource to another Resource

# Attributes:
#     capacity (IsBnd): bound on the capacity of the Operation
#     produce (IsBnd): bounded by capacity of Process. Reported by Operate as well
#     buy (IsBnd): bound on amount of Resource bought by Process
#     sell (IsBnd): bound on amount of Resource sold by Process
#     use (IsBnd): bound on amount of Land or Material used by Process
#     setup_use (IsExt): Land or Material setup_use per unit capacity
#     use_emission (IsExt): emission due to land or Material use
#     capex (IsInc): capital expense per Capacitate
#     opex (IsInc): operational expense based on Operation
#     setup_emission (IsExt): emission due to construction activity
#     buy_price (IsInc): price to buy per unit basis
#     sell_price (IsInc): price at which to sell per unit basis
#     credit (IsExt): credit received per unit basis sold
#     penalty (IsExt): penalty paid for not meeting lower bound of sell
#     conversion (IsCnv): conversion of Resource to other Resources
#     locations (list[Location]): locations where the Process is located
#     basis (str): basis of the component
#     citation (dict): citation of the component
#     block (str): block of the component
#     introduce (str): index in scale when the component is introduced
#     retire (str): index in scale when the component is retired
#     label (str): label of the component

# """

from __future__ import annotations

from typing import TYPE_CHECKING

from gana.sets.variable import V

from ...decisions.action import Act
from ..commodity.resource import Conv, Resource
from ..impact.econ import Econ
from ..impact.environ import Environ
from ..impact.social import Social
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..space.location import Loc
    from ..time.period import Period


class Balance:
    def __init__(self, process: Process):
        self.process = process

        self.resource: Resource = None

    @property
    def network(self):
        """Circumscribing Loc"""
        return self.process.network

    @property
    def horizon(self):
        """Circumscribing Period"""
        return self.process.horizon

    @property
    def prg(self):
        return self.process.prg

    def __call__(self, resource: Resource):
        self.resource = resource
        return self

    def __eq__(self, other: Conv):
        setattr(
            self.prg,
            'produce',
            V(
                self.resource.x,
                self.process.x,
                self.network.x,
                self.horizon.xset,
                mutable=True,
            ),
        )
        exp = getattr(self.prg, 'produce')(
            self.resource.x, self.process.x, self.network.x, self.horizon.xset
        )
        if not isinstance(other.res, list):
            res_ = [other.res]
            mul_ = [other.mul]
        else:
            res_ = other.res
            mul_ = other.mul
        for res, par in zip(res_, mul_):
            if par > 0:
                setattr(
                    self.prg,
                    'produce',
                    V(
                        res.x,
                        self.process.x,
                        self.network.x,
                        self.horizon.xset,
                        mutable=True,
                    ),
                )
                exp += par * getattr(self.prg, 'produce')(
                    res.x, self.process.x, self.network.x, self.horizon.xset
                )
            if par < 0:
                setattr(
                    self.prg,
                    'consume',
                    V(
                        res.x,
                        self.process.x,
                        self.network.x,
                        self.horizon.xset,
                        mutable=True,
                    ),
                )
                exp -= -par * getattr(self.prg, 'consume')(
                    res.x, self.process.x, self.network.x, self.horizon.xset
                )

        setattr(self.prg, self.process.name + '_conv', exp == 0)


class Process(ModCmp):
    """Process converts one Resource to another Resource"""

    def __init__(self, basis: Basis = None, label: str = None):
        self.basis = basis

        ModCmp.__init__(self, label)

        self.setup = Act([Resource], [Econ, Environ, Social])
        self.dismantle = -self.setup

        self.operate = Act([Resource], [Econ, Environ, Social])

        self.conv = Balance(self)
