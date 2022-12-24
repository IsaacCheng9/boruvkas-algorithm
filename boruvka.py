"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from collections import defaultdict
from typing import List


class Graph:
    def __init__(self, vertices: set, edges: List[tuple]):
        self.vertices = vertices
        # [node_from, node_to, weight]
        self.edges = edges

        # Build the initial adjacency list according to the edges provided.
        # node_from: {
        #   node_to: weight,
        #   node_to: weight,
        # }
        self.adjacency_list = defaultdict(lambda: defaultdict(int))
        for edge in edges:
            self.adjacency_list[edge[0]][edge[1]] = edge[2]

    def get_vertices(self) -> set:
        return self.vertices

    def get_edges(self) -> List[tuple]:
        return self.edges

    def get_adjacency_list(self) -> dict:
        return self.adjacency_list

    def add_vertex(self, vertex: str) -> bool:
        if vertex in self.vertices:
            raise ValueError(f"Vertex {vertex} already exists")

        self.vertices.add(vertex)
        return True

    def add_edge(self, node_from: str, node_to: str, weight: int) -> bool:
        if node_to in self.adjacency_list[node_from]:
            raise ValueError(f"An edge from {node_from} to {node_to} already exists")

        self.adjacency_list[node_from][node_to] = weight
        self.edges.append((node_from, node_to, weight))
        return True


class Boruvka:
    def __init__(self, graph: Graph):
        self.graph = graph

    def find_mst(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
