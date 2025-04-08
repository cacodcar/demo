"""Inventory Space"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..core.sample import Index

if TYPE_CHECKING:
    from ..operation.process import Process
    from ..operation.storage import Storage
    from ..operation.transit import Transit


@dataclass
class Inv(Index):
    """Inventory space of Operations"""

    operation: Process | Storage | Transit = None

    def __post_init__(self):
        Index.__post_init__(self)
