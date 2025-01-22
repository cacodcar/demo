"""Conversion of a resource"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..components.commodity.resource import Resource
    from ..components.task.process import Process


class Conv:
    """Conversion of a resource into another"""

    def __init__(self, resource: Resource = None, process: Process = None):

        self.resource = resource
        self.process = process
