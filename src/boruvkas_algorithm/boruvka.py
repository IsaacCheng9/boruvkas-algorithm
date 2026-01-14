"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""

import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    """A graph that contains nodes and edges."""

    def __init__(self, num_nodes: int) -> None:
        """
        Initialises the graph with a given number of vertices.

        Args:
            num_nodes: The number of nodes to generate in the graph.
        """
        self.vertices: list[int] = list(range(num_nodes))
        # [(node1, node2, weight)]
        self.edges: list[tuple[int, int, int]] = []

    def add_edge(self, node1: int, node2: int, weight: int) -> None:
        """
        Adds an edge to the graph.

        Args:
            node1: The first node of the edge.
            node2: The second node of the edge.
            weight: The weight of the edge.

        Raises:
            ValueError: If either node does not exist in the graph.
        """
        if node1 not in self.vertices or node2 not in self.vertices:
            raise ValueError("One or both vertices not found in graph.")
        self.edges.append((node1, node2, weight))

    def print_graph_info(self) -> None:
        """Print the graph's vertices and edges."""
        print(f"Vertices: {self.vertices}")
        print("Edges (node1, node2, weight):")
        for edge in sorted(self.edges):
            print(f"    {edge}")

    def draw_mst(self, mst_edges: list[tuple[int, int, int]]) -> None:
        """
        Draw the graph with the minimum spanning tree highlighted using
        networkx.

        Args:
            mst_edges: A list of edges in the minimum spanning tree.
        """
        G = nx.Graph()
        # Add nodes to the graph.
        G.add_nodes_from(self.vertices)
        # Add all edges to the graph with weights.
        for edge in self.edges:
            node1, node2, weight = edge
            G.add_edge(node1, node2, weight=weight)
        pos = nx.spring_layout(G)
        # Draw the graph edges and highlight the edges in the MST in red.
        nx.draw_networkx_edges(
            G, pos, edgelist=self.edges, edge_color="gray", alpha=0.5
        )
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color="red", width=2)
        # Draw the graph nodes and labels.
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        )

        plt.title("Graph with Minimum Spanning Tree Highlighted")
        plt.axis("off")
        plt.show()


def find_mst_with_boruvkas_algorithm(
    graph: Graph,
) -> tuple[int, list[tuple[int, int, int]]]:
    """
    Finds the minimum spanning tree (MST) of a graph using Boruvka's algorithm.

    Args:
        graph: The graph to find the MST of.

    Returns:
        A tuple containing the total weight of the MST and a list of the
        edges in the MST.
    """

    def find(node: int) -> int:
        """
        Finds the root parent of the node using path compression.

        Args:
            node: The node to find the root parent of.

        Returns:
            The root parent of the node.
        """
        cur_parent = parent[node]
        while cur_parent != parent[cur_parent]:
            # Compress the links as we go up the chain of parents to make
            # it faster to traverse in the future - amortised O(a(n)) time,
            # where a(n) is the inverse Ackermann function.
            parent[cur_parent] = parent[parent[cur_parent]]
            cur_parent = parent[cur_parent]
        return cur_parent

    def union(node1: int, node2: int) -> bool:
        """
        Combines the two nodes into the larger segment.

        Args:
            node1: The first node to combine.
            node2: The second node to combine.

        Returns:
            True if the nodes were combined, False if they were already in the
            same segment.
        """
        root1 = find(node1)
        root2 = find(node2)
        # If they have the same root parent, they're already connected.
        if root1 == root2:
            return False

        # Combine the two nodes into the larger segment based on the rank.
        if rank[root1] > rank[root2]:
            parent[root2] = root1
            rank[root1] += rank[root2]
        else:
            parent[root1] = root2
            rank[root2] += rank[root1]
        return True

    num_vertices = len(graph.vertices)
    # Each node is its own parent initially.
    parent: list[int] = list(range(num_vertices))
    # Each tree has size 1 (itself) initially.
    rank: list[int] = [1] * num_vertices

    print("\nFinding MST with Boruvka's algorithm:")
    graph.print_graph_info()

    mst_weight = 0
    mst_edges: list[tuple[int, int, int]] = []
    num_components = num_vertices
    num_iterations = 0

    # Keep connecting components until only one component remains.
    while num_components > 1:
        num_iterations += 1
        print(
            f"\nIteration {num_iterations}:\nCurrent MST edges: {mst_edges}\n"
            f"Current MST Weight: {mst_weight}"
        )

        # Find the minimum connecting edge for each component.
        min_edge_per_component: list[tuple[int, int, int] | None] = [
            None
        ] * num_vertices
        for edge in graph.edges:
            node1, node2, weight = edge
            comp1, comp2 = find(node1), find(node2)

            if comp1 != comp2:
                current_min1 = min_edge_per_component[comp1]
                if current_min1 is None or weight < current_min1[2]:
                    min_edge_per_component[comp1] = edge
                current_min2 = min_edge_per_component[comp2]
                if current_min2 is None or weight < current_min2[2]:
                    min_edge_per_component[comp2] = edge

        # Connect components using the minimum connecting edges.
        for edge in min_edge_per_component:
            if edge is not None:
                node1, node2, weight = edge
                if find(node1) != find(node2):
                    mst_edges.append(edge)
                    mst_weight += weight
                    union(node1, node2)
                    num_components -= 1
                    print(f"Added edge {node1} - {node2} with weight {weight} to MST.")

    # Summarise the MST found.
    print("\nMST found with Boruvka's algorithm.")
    print("MST edges (node1, node2, weight):")
    for edge in sorted(mst_edges):
        print(f"    {edge}")
    print(f"MST weight: {mst_weight}")

    return mst_weight, mst_edges


def run_boruvka_example():
    """Runs Boruvka's algorithm on an example graph."""
    graph = Graph(9)
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 6, 7)
    graph.add_edge(1, 6, 11)
    graph.add_edge(1, 7, 20)
    graph.add_edge(1, 2, 9)
    graph.add_edge(2, 3, 6)
    graph.add_edge(2, 4, 2)
    graph.add_edge(3, 4, 10)
    graph.add_edge(3, 5, 5)
    graph.add_edge(4, 5, 15)
    graph.add_edge(4, 7, 1)
    graph.add_edge(4, 8, 5)
    graph.add_edge(5, 8, 12)
    graph.add_edge(6, 7, 1)
    graph.add_edge(7, 8, 3)

    _, mst_edges = find_mst_with_boruvkas_algorithm(graph)
    # Draw the graph with the minimum spanning tree highlighted.
    graph.draw_mst(mst_edges)


if __name__ == "__main__":
    run_boruvka_example()
