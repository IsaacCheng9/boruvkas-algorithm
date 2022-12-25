"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from typing import List


class Graph:
    def __init__(self, vertices: set, edges: List[tuple]):
        self.vertices = vertices
        # [(node1, node2, weight)]
        self.edges = edges
        self.components = {}

    def get_vertices(self) -> set:
        return self.vertices

    def get_edges(self) -> List[tuple]:
        return self.edges

    def add_vertex(self, vertex: str) -> bool:
        if vertex in self.vertices:
            raise ValueError(f"Vertex {vertex} already exists")

        self.vertices.add(vertex)
        return True

    def add_edge(self, node1: str, node2: str, weight: int) -> bool:
        self.edges.append((node1, node2, weight))
        return True

    def find_mst_with_boruvka(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
