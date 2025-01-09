"""Graph"""

from ..components.graph.edge import Edge
from ..components.graph.node import Node
from .rep import Rep


class Graph(Rep):
    """Graph representation"""

    def __init__(self):

        Rep.__init__(self)

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
