"""Default decisions"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bind import Bind


class Get:
    """Get the Decision"""

    def get(self, decision: str):
        """Get the decision"""
        return getattr(getattr(self, 'design'), decision)(self)


class Capacitate(Get):
    """Capacitate an Operation"""

    @property
    def setup(self):
        """Add Capacity"""
        return self.get('setup')

    @property
    def dismantle(self):
        """Remove Capacity"""
        return self.get('dismantle')


class Trade(Get):
    """Exchange Resource/Material with another Player"""

    @property
    def buy(self):
        return self.get('buy')

    @property
    def sell(self):
        return self.get('sell')


class Transact(Get):
    """Exchange Cash with another Player"""

    @property
    def earn(self):
        return self.get('earn')

    @property
    def spend(self):
        return self.get('spend')


class Operate(Get):
    """Operate an Operation"""

    @property
    def operate(self):
        return self.get('operate')


class Produce(Get):
    """Resource Flow resulting from Operate"""

    @property
    def produce(self):
        return self.get('produce')

    @property
    def consume(self):
        return self.get('consume')


class Stock(Get):
    """Inventory of a Resource"""

    @property
    def inventory(self):
        return self.get('inventory')


class Ship(Get):
    """Resource Flow between Locations"""

    @property
    def export(self):
        return self.get('export')


class EnvImp(Get):
    """Environemntal Impact"""

    @property
    def emit(self):
        return self.get('emit')

    @property
    def abate(self):
        return self.get('abate')


class SocImp(Get):
    """Soc Impact"""

    @property
    def benefit(self):
        return self.get('benefit')

    @property
    def detriment(self):
        return self.get('detriment')


class Utilize(Get):
    """Usage of a Resource"""

    @property
    def use(self):
        return self.get('use')

    @property
    def dispose(self):
        return self.get('stock')
