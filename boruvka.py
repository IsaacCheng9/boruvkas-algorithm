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

    def add_edge(self, node1: str, node2: str, weight: int) -> bool:
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} does not exist")
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} does not exist")

        self.edges.append((node1, node2, weight))
        return True

    def find_mst_with_boruvka(self):
        pass


def main():
    # https://www.statisticshowto.com/boruvkas-algorithm/
    graph1 = Graph(9)
    graph1.find_mst_with_boruvka()


if __name__ == "__main__":
    main()
