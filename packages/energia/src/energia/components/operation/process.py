"""Process converts one Resource to another Resource
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...decisions.balance import Bal
from ...decisions.default import Capacitate, Operate
from ..core.modeling import Component
from ..spatial.inventory import Inv

if TYPE_CHECKING:
    from ..commodity.resource import Resource
    from ..measure.basis import Unit


@dataclass
class Process(Component, Capacitate, Operate):
    """Process converts one Resource to another Resource"""

    def __post_init__(self):
        Capacitate.__init__(self)
        Component.__post_init__(self)
        self._conv = False
        self.conv = None

    def __setattr__(self, name, value):
        if value:
            if name == 'model':
                setattr(value, f'Cap({self.name})', Inv(operation=self))

        super().__setattr__(name, value)

    @property
    def base(self) -> Resource:
        """Base resource"""
        return self.conv.base

    @property
    def balance(self) -> dict[Resource : int | float]:
        """Balance of commodities"""
        return self.conv.balance

    def __call__(self, thing: Resource | Bal):
        """Bal is called with a Resource to be converted"""
        if not self._conv:
            self.conv = Bal(process=self)
            self._conv = True
        return self.conv(thing)
