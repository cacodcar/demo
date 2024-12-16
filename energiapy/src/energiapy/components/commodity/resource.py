"""Resource are: 
    1. converted by Processes
    2. stored by Storage
    3. transported by Transits
    4. lost by Storage and Transits
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from ...decisions.flow import Flow
from ..impact.econ import Econ
from ..impact.environ import Environ
from ..impact.social import Social
from ..types.modeling import ModCmp

if TYPE_CHECKING:
    from ..measure.basis import Basis


class Trade:
    """Trade a Resource"""

    def __init__(self):

        self.buy = Flow([Econ, Environ, Social])
        self.sell = -self.buy


class Use:
    """Use a Resource"""

    def __init__(self):
        self.use = Flow([Econ, Environ, Social])
        self.dispose = -self.use


class Ship:
    """Ship a Resource"""

    def __init__(self):
        self.receive = Flow([Econ, Environ, Social])
        self.ship = -self.receive


class Lose:
    """Lose a Resource"""

    def __init__(self):
        self.recover = Flow([Econ, Environ, Social])
        self.lose = -self.recover


class Produce:
    """Operate a Resource"""

    def __init__(self):
        self.consume = Flow([Econ, Environ, Social])
        self.produce = -self.consume


class Conv:
    def __init__(self, res, mul):
        self.res: Resource | list[Resource] = res
        self.mul: int | list[Resource] = mul

    def __add__(self, other: Conv):
        if not isinstance(self.res, list):
            res = [self.res]
            mul = [self.mul]
        else:
            res = self.res
            mul = self.mul

        if not isinstance(other.res, list):
            res2 = [other.res]
            mul2 = [other.mul]
        else:
            res2 = other.res
            mul2 = other.mul
        return Conv(res + res2, mul + mul2)

    def __neg__(self):
        if isinstance(self.res, list):
            mul = self.mul
            mul[0] = -self.mul[0]
        else:
            mul *= -1
        return Conv(self, mul)

    def __sub__(self, other: Conv):
        if not isinstance(self.res, list):
            res = [self.res]
            mul = [self.mul]
        else:
            res = self.res
            mul = self.mul
        if not isinstance(other.res, list):
            res2 = [other.res]
            mul2 = [-other.mul]
        else:
            res2 = other.res
            mul2 = other.mul
            mul2[0] = -mul2[0]

        return Conv(res + res2, mul + mul2)


class Resource(ModCmp, Trade, Use, Ship, Lose, Produce):
    """A resource, can be a material, chemical, energy, etc."""

    def __init__(self, basis: Basis = None, label: str = None):

        self.basis = basis

        ModCmp.__init__(self, label)
        Trade.__init__(self)
        Use.__init__(self)
        Ship.__init__(self)
        Lose.__init__(self)
        Produce.__init__(self)

        self.mul: int | float = 1

    def __mul__(self, other: int | float):
        return Conv(self, other)

    def __rmul__(self, other: int | float):
        return self * other

    def __add__(self, other: Conv):
        return Conv([self, other.res], [self.mul, other.mul])

    def __neg__(self):
        self.mul *= -1
        return Conv(self, self.mul * -1)

    def __sub__(self, other: Conv):
        return Conv([self, other.res], [self.mul, -other.mul])
