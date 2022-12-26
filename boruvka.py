"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from typing import List


class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.nodes = [node for node in range(1, num_nodes + 1)]
        # [(node1, node2, weight)]
        self.edges = []
        # {node: parent} to represent the component trees. Initially, each node
        # is its own parent, as the graph is disconnected.
        self.components = {node: node for node in self.nodes}

    def get_nodes(self) -> list:
        return self.nodes

    def get_edges(self) -> List[tuple]:
        return self.edges

    def add_edge(self, node1: int, node2: int, weight: int) -> bool:
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} does not exist")
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} does not exist")

        self.edges.append((node1, node2, weight))
        return True

    def find_mst_with_boruvka(self):
        pass


def main():
    graph1 = Graph(9)
    graph1.add_edge(0, 1, 4)
    graph1.add_edge(0, 6, 7)
    graph1.add_edge(1, 6, 11)
    graph1.add_edge(1, 7, 20)
    graph1.add_edge(1, 2, 9)
    graph1.add_edge(2, 3, 6)
    graph1.add_edge(2, 4, 2)
    graph1.add_edge(3, 4, 10)
    graph1.add_edge(3, 5, 5)
    graph1.add_edge(4, 5, 15)
    graph1.add_edge(4, 7, 1)
    graph1.add_edge(4, 8, 5)
    graph1.add_edge(5, 8, 12)
    graph1.add_edge(6, 7, 1)
    graph1.add_edge(7, 8, 3)
    graph1.find_mst_with_boruvka()


if __name__ == "__main__":
    main()
