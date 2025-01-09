"""Interaction between different actions"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..components.commodity.resource import Resource
    from ..components.task.process import Process


class Conversion:
    """Balance of resources"""

    def __init__(self):
        # set up
        self.process: Process = None

    @property
    def name(self):
        """Name"""
        return f'η({self.process})'

    def __call__(self, resource: Resource):
        """Return the conversion rate"""
        return resource.produce(
            resource.x,
            self.process.x,
            self.process.network.x,
            self.process.horizon.xset,
        )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
