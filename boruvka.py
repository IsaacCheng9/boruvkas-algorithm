"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from typing import List


class Graph:
    def __init__(self, nodes: set = set(), edges: List[tuple] = []):
        self.nodes = nodes
        # [(node1, node2, weight)]
        self.edges = edges
        self.components = {}

    def get_nodes(self) -> set:
        return self.nodes

    def get_edges(self) -> List[tuple]:
        return self.edges

    def add_node(self, node: str) -> bool:
        if node in self.nodes:
            raise ValueError(f"Node {node} already exists")

        self.nodes.add(node)
        return True

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
    graph1 = Graph()
    for node in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
        graph1.add_node(node)
    graph1.add_edge("A", "B", 1)
    graph1.add_edge("A", "E", 7)
    graph1.add_edge("B", "C", 2)
    graph1.add_edge("B", "F", 8)
    graph1.add_edge("B", "G", 9)
    graph1.add_edge("C", "D", 3)
    graph1.add_edge("C", "H", 1)
    graph1.add_edge("D", "H", 2)
    graph1.add_edge("E", "F", 4)
    graph1.add_edge("E", "I", 4)
    graph1.add_edge("E", "J", 8)
    graph1.add_edge("F", "G", 5)
    graph1.add_edge("F", "J", 3)
    graph1.add_edge("F", "K", 4)
    graph1.add_edge("G", "H", 6)
    graph1.add_edge("G", "K", 9)
    graph1.add_edge("H", "L", 5)
    graph1.add_edge("K", "L", 6)
    graph1.find_mst_with_boruvka()


if __name__ == "__main__":
    main()
