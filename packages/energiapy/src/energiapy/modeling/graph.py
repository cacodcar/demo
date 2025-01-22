"""Graph"""

from dataclasses import dataclass

from ..components._core.tag import Name
from ..components.graph.edge import Edge
from ..components.graph.node import Node


@dataclass
class Graph(Name):
    """Graph representation"""

    def __post_init__(self):
        self.nodes = []
        self.edges = []

    def __setattr__(self, name, value):
        if isinstance(value, Node):
            value.name = name
            value.graph = self
            self.nodes.append(value)
        elif isinstance(value, Edge):
            value.name = name
            value.graph = self
            self.edges.append(value)

        super().__setattr__(name, value)
