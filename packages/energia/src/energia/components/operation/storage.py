"""Storage - Stashes Resource to Withdraw Later
"""

from dataclasses import dataclass

from ...decisions.balance import Bal
from ...decisions.default import Capacitate, Operate, Stock
from ..commodity.resource import Resource
from ..core.modeling import Component
from ..spatial.inventory import Inv
from .process import Process


@dataclass
class Storage(Component, Capacitate, Operate, Stock):
    """Storage"""

    store: Resource = None

    def __post_init__(self):
        Component.__post_init__(self)
        self.stored = None
        self._conv = False
        self.conv = None
        self.charge = Process()
        self.discharge = Process()
        self.inv = Inv(operation=self)

    def __setattr__(self, name, value):
        if name == 'model' and value:
            setattr(value, f'{self.name}.charge', self.charge)
            setattr(value, f'{self.name}.discharge', self.discharge)
            setattr(value, f'Cap({self.name})', self.inv)

        super().__setattr__(name, value)

    @property
    def base(self) -> Resource:
        """Base resource"""
        return self.discharge.conv.base

    @property
    def balance(self) -> dict[Resource : int | float]:
        """Balance of commodities"""
        return self.discharge.conv.balance

    def __call__(self, thing: Resource | Bal):
        """Bal is called with a Resource to be converted"""
        if not self._conv:
            stored = Resource()
            setattr(self.model, f'{thing}.stored', stored)
            self.discharge.conv = Bal(process=self.discharge, resource=stored)
            self.discharge.conv(thing)
            self.base.stored = stored
            self.stored = stored
            self._conv = True

            self.charge.conv = Bal(process=self.charge, storage=self, resource=thing)
            self.charge.conv(stored) == -1.0 * thing

        return self.discharge.conv(thing)
