import random
import numpy as np
from graphviz import Digraph


class Plant:
    def __init__(self, width, height, orientation, dna, parent=None, master=None):
        """
        Initializes a Plant node.

        Args:
            width (float): The width of the plant node.
            height (float): The height of the plant node.
            orientation (float): The orientation of the plant node.
            dna (dict): Growth rules for the plant.
            parent (Plant, optional): The parent node. Defaults to None.
            master (Plant, optional): The master or root node of the plant. Defaults to None.
        """
        self.width = width
        self.height = height
        self.orientation = orientation
        self.dna = dna
        self.children = []
        self.parent = parent
        self.master = master if master else self

        if parent:
            parent.add_child(self)

    def add_child(self, child):
        """
        Adds a child node to the current plant node.

        Args:
            child (Plant): The child node to be added.
        """
        self.children.append(child)

    def grow(self, time_simulated):
        """
        Simulates the growth of the plant over a specified time period.

        Args:
            time_simulated (int): The number of growth cycles to simulate.
        """
        for _ in range(time_simulated):
            new_children = []
            for node in list(self.traverse()):
                if node.children:
                    height_increment = (
                        random.gammavariate(2, node.height)
                        * self.dna['height_growth_multiplier']
                    )
                    width_increment = (
                        random.gammavariate(2, node.width)
                        * self.dna['weight_growth_multiplier']
                    )
                    node.height = min(node.height + height_increment, self.dna['max_height'])
                    node.width = min(node.width + width_increment, self.dna['max_width'])
                else:
                    num_children = max(
                        0,
                        int(random.gauss(self.dna['normal_mean_branch'], self.dna['normal_std_branch']))
                    )
                    for _ in range(num_children):
                        child_orientation = random.gauss(
                            self.dna['normal_mean_orientation'], self.dna['normal_std_orientation']
                        )
                        new_child = Plant(
                            width=1,
                            height=1.5,
                            orientation=child_orientation,
                            dna=self.dna,
                            parent=node,
                            master=self.master,
                        )
                        new_children.append(new_child)

            for child in new_children:
                if child not in child.parent.children:
                    child.parent.add_child(child)

    def traverse(self, visited=None):
        """
        Traverses the plant tree in a depth-first manner.

        Args:
            visited (set, optional): A set of visited nodes to avoid cycles. Defaults to None.

        Yields:
            Plant: The current plant node being traversed.
        """
        if visited is None:
            visited = set()

        if self in visited:
            return

        visited.add(self)
        yield self

        for child in self.children:
            yield from child.traverse(visited)

    def export_to_graphviz(self, graph=None):
        """
        Exports the plant structure to a Graphviz graph.

        Args:
            graph (Digraph, optional): An existing Graphviz graph. Defaults to None.

        Returns:
            Digraph: A Graphviz graph representing the plant structure.
        """
        if graph is None:
            graph = Digraph(format="png")
            graph.attr(rankdir="BT")  # Cambiar la orientación de arriba a abajo a abajo a arriba

        # Incluir el atributo de orientación en la representación del nodo
        graph.node(str(id(self)), f"Width={self.width:.2f}\nHeight={self.height:.2f}\nOrientation={self.orientation}")

        for child in self.children:
            graph.edge(str(id(self)), str(id(child)))
            child.export_to_graphviz(graph)

        return graph