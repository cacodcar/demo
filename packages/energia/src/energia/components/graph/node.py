"""Node"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..core.tag import Name

if TYPE_CHECKING:
    from ...modeling.graph import Graph


@dataclass
class Node(Name):
    """Node of a graph"""

    def __post_init__(self):

        self.graph: Graph = None
