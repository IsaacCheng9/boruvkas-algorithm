"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""

import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, num_vertices: int):
        """
        Args:
            num_vertices: The number of vertices to generate in the graph.
        """
        self.vertices: list[int] = list(range(num_vertices))
        # [(node1, node2, weight)]
        self.edges: list[tuple[int, int, int]] = []
        # Each node is its own parent initially.
        self.parent: list[int] = list(range(num_vertices))
        # Each tree has size 1 (itself) initially.
        self.rank: list[int] = [1] * num_vertices

    def add_edge(self, node1: int, node2: int, weight: int) -> None:
        """
        Add an edge to the graph.

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
        """
        Print the graph's vertices and edges.
        """
        print(f"Vertices: {self.vertices}")
        print("Edges (node1, node2, weight):")
        for edge in sorted(self.edges):
            print(f"    {edge}")

    def find(self, node: int) -> int:
        """
        Finds the root parent of the node using path compression.

        Args:
            node: The node to find the root parent of.

        Returns:
            The root parent of the node.
        """
        cur_parent = self.parent[node]
        while cur_parent != self.parent[cur_parent]:
            # Compress the links as we go up the chain of parents to make
            # it faster to traverse in the future - amortised O(a(n)) time,
            # where a(n) is the inverse Ackermann function.
            self.parent[cur_parent] = self.parent[self.parent[cur_parent]]
            cur_parent = self.parent[cur_parent]

        return cur_parent

    def union(self, node1: int, node2: int) -> bool:
        """
        Combines the two nodes into the larger segment.

        Args:
            node1: The first node to combine.
            node2: The second node to combine.

        Returns:
            True if the nodes were combined, False if they were already in the
            same segment.
        """
        root1 = self.find(node1)
        root2 = self.find(node2)
        # If they have the same root parent, a cycle exists.
        if root1 == root2:
            return False

        # Combine the two nodes into the larger segment based on the rank.
        if self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
            self.rank[root1] += self.rank[root2]
        else:
            self.parent[root1] = root2
            self.rank[root2] += self.rank[root1]

        return True

    def update_min_edge_per_component(self, min_connecting_edge_per_component: list):
        """
        Check each edge and update the shortest edge for each node if it
        connects two components together.

        Args:
            min_connecting_edge_per_component: A list with the shortest edge
                                               for each node that connects to
                                               a new component.
        """
        for edge in self.edges:
            node1, node2, weight = edge
            node1_component = self.find(node1)
            node2_component = self.find(node2)

            # If the vertices are in different components and the edge is
            # smaller than the current minimum weight edge for either
            # component, update them.
            if node1_component != node2_component:
                if (
                    not min_connecting_edge_per_component[node1_component]
                    or weight < min_connecting_edge_per_component[node1_component][2]
                ):
                    min_connecting_edge_per_component[node1_component] = edge

                if (
                    not min_connecting_edge_per_component[node2_component]
                    or weight < min_connecting_edge_per_component[node2_component][2]
                ):
                    min_connecting_edge_per_component[node2_component] = edge

    def connect_components_with_min_edges(
        self,
        min_connecting_edge_per_component: list,
        mst_edges: list[tuple[int, int, int]],
        mst_weight: int,
        num_components: int,
    ) -> tuple[int, int]:
        """
        Connect components using the minimum connecting edges.

        Args:
            min_connecting_edge_per_component: List storing the shortest edge
                                               for each component.
            mst_edges: List of edges in the minimum spanning tree.
            mst_weight: Total weight of the minimum spanning tree.
            num_components: Total number of components in the graph.

        Returns:
            Tuple containing the updated MST weight and number of components.
        """
        for edge in min_connecting_edge_per_component:
            if edge is not None:
                node1, node2, weight = edge
                if self.find(node1) != self.find(node2):
                    mst_edges.append((node1, node2, weight))
                    mst_weight += weight
                    self.union(node1, node2)
                    num_components -= 1
                    print(f"Added edge {node1} - {node2} with weight {weight} to MST.")

        return mst_weight, num_components

    def perform_iteration(
        self,
        num_components: int,
        mst_edges: list[tuple[int, int, int]],
        mst_weight: int,
    ):
        """
        Perform one iteration of Boruvka's algorithm, finding the minimum
        connecting edge for each component and connecting components using
        these edges.

        Args:
            num_components: Total number of components in the graph.
            mst_edges: List of edges in the minimum spanning tree so far.
            mst_weight: Total weight of the minimum spanning tree so far.

        Returns:
            Tuple containing the updated MST weight and number of components.
        """
        # Initialize list to store minimum connecting edge for each component.
        min_connecting_edge_per_component = [None] * len(self.vertices)
        # Update the minimum connecting edge for each component.
        self.update_min_edge_per_component(min_connecting_edge_per_component)
        # Connect components using the minimum connecting edges and update MST
        # weight and number of components.
        mst_weight, num_components = self.connect_components_with_min_edges(
            min_connecting_edge_per_component,
            mst_edges,
            mst_weight,
            num_components,
        )

        return mst_weight, num_components

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

    def run_boruvkas_algorithm(self):
        """
        Find the minimum spanning tree (MST) of the graph using Boruvka's
        algorithm.

        Returns:
            A tuple containing the total weight of the MST and a list of the
            edges in the MST.
        """
        print("\nFinding MST with Boruvka's algorithm:")
        self.print_graph_info()
        mst_weight = 0
        mst_edges = []
        num_components = len(self.vertices)
        # Track the number of iterations.
        num_iterations = 0

        # Keep connecting components until only one component remains.
        while num_components > 1:
            num_iterations += 1
            print(
                f"\nIteration {num_iterations}:\nCurrent MST edges: {mst_edges}\n"
                f"Current MST Weight: {mst_weight}"
            )
            # Perform one iteration of the algorithm.
            mst_weight, num_components = self.perform_iteration(
                num_components,
                mst_edges,
                mst_weight,
            )

        # Summarise the MST found.
        print("\nMST found with Boruvka's algorithm.")
        print("MST edges (node1, node2, weight):")
        for edge in sorted(mst_edges):
            print(f"    {edge}")
        print(f"MST weight: {mst_weight}")

        return mst_weight, mst_edges


def main():
    """
    Run Boruvka's algorithm on an example graph.
    """
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
    _, mst_edges = graph.run_boruvkas_algorithm()
    # Draw the graph with the minimum spanning tree highlighted.
    graph.draw_mst(mst_edges)


if __name__ == "__main__":
    main()
