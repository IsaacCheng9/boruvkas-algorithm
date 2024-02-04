"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
import matplotlib.pyplot as plt
import networkx as nx

from typing import Dict, List, Optional, Tuple


class Graph:
    """
    A graph that contains vertices and edges.
    """

    def __init__(self, num_vertices: int):
        """
        Args:
            num_vertices: The number of vertices to generate in the graph.
        """
        self.vertices = list(range(num_vertices))
        # [(vertex_1, vertex_2, weight)]
        self.edges = []

    def add_edge(self, vertex_1: int, vertex_2: int, weight: int) -> None:
        """
        Add an edge to the graph.

        Args:
            vertex_1: The first vertex of the edge.
            vertex_2: The second vertex of the edge.
            weight: The weight of the edge.

        Raises:
            ValueError: If either vertex does not exist in the graph.
        """
        if vertex_1 not in self.vertices or vertex_2 not in self.vertices:
            raise ValueError("One or both vertices not found in graph.")
        self.edges.append((vertex_1, vertex_2, weight))

    def print_graph_info(self) -> None:
        """
        Print the graph's vertices and edges.
        """
        print(f"Vertices: {self.vertices}")
        print("Edges (vertex_1, vertex_2, weight):")
        for edge in sorted(self.edges):
            print(f"    {edge}")

    def merge_components(
        self,
        vertex_to_component: Dict[int, int],
        component_sizes: List[int],
        vertex_1: int,
        vertex_2: int,
    ) -> None:
        """
        Merge two components of the graph into one, ensuring that the smaller
        component is merged into the larger one to optimize the merging
        process.

        Args:
            vertex_to_component: A mapping of vertices to their component
                                 identifiers.
            component_sizes: A list where the index represents the component
                             identifier and the value is the size of the
                             component.
            vertex_1: A vertex in the first component to be merged.
            vertex_2: A vertex in the second component to be merged.
        """
        # Identify the components of the two vertices.
        component_1 = vertex_to_component[vertex_1]
        component_2 = vertex_to_component[vertex_2]

        # Determine the smaller and larger components.
        if component_sizes[component_1] < component_sizes[component_2]:
            smaller, larger = component_1, component_2
        else:
            smaller, larger = component_2, component_1

        # Merge the smaller component into larger component.
        for vertex, component in vertex_to_component.items():
            if component == smaller:
                vertex_to_component[vertex] = larger
        # Update the size of the larger component.
        component_sizes[larger] += component_sizes[smaller]

    def update_min_edge_per_component(
        self,
        vertex_to_component: Dict[int, int],
        min_connecting_edge_per_component: List[Optional[Tuple]],
    ):
        """
        Check each edge and update the shortest edge for each vertex if it
        connects two components together.

        Args:
            vertex_to_component: A dictionary containing the component of each
                                 vertex.
            min_connecting_edge_per_component: A list with the shortest edge
                                               for each vertex that connects to
                                               a new component.
        """
        for edge in self.edges:
            vertex_1, vertex_2, weight = edge
            vertex_1_component = vertex_to_component[vertex_1]
            vertex_2_component = vertex_to_component[vertex_2]

            # If the vertices are in different components and the edge is
            # smaller than the current minimum weight edge for either
            # component, update them.
            if vertex_1_component != vertex_2_component:
                if (
                    not min_connecting_edge_per_component[vertex_1_component]
                    or weight < min_connecting_edge_per_component[vertex_1_component][2]
                ):
                    min_connecting_edge_per_component[vertex_1_component] = edge

                if (
                    not min_connecting_edge_per_component[vertex_2_component]
                    or weight < min_connecting_edge_per_component[vertex_2_component][2]
                ):
                    min_connecting_edge_per_component[vertex_2_component] = edge

    def connect_components_with_min_edges(
        self,
        component_sizes: List[int],
        min_connecting_edge_per_component: List[Optional[Tuple]],
        mst_edges: List[Tuple[int, int, int]],
        mst_weight: int,
        vertex_to_component: Dict[int, int],
        num_components: int,
    ) -> Tuple[int, int]:
        """
        Connect components using the minimum connecting edges.

        Args:
            component_sizes: List containing the sizes of each component.
            min_connecting_edge_per_component: List storing the shortest edge
                                               for each component.
            mst_edges: List of edges in the minimum spanning tree.
            mst_weight: Total weight of the minimum spanning tree.
            vertex_to_component: Dictionary mapping vertices to their
                                 component.
            num_components: Total number of components in the graph.

        Returns:
            Tuple containing the updated MST weight and number of components.
        """
        for edge in min_connecting_edge_per_component:
            if edge is not None:
                vertex_1, vertex_2, weight = edge
                if vertex_to_component[vertex_1] != vertex_to_component[vertex_2]:
                    mst_edges.append((vertex_1, vertex_2, weight))
                    mst_weight += weight
                    self.merge_components(
                        vertex_to_component, component_sizes, vertex_1, vertex_2
                    )
                    num_components -= 1
                    print(
                        f"Added edge {vertex_1} - {vertex_2} with "
                        f"weight {weight} to MST."
                    )

        return mst_weight, num_components

    def initialize_components(self) -> Tuple[Dict[int, int], List[int], int]:
        """
        Initialize each vertex as its own component with size 1, and set the
        initial number of components equal to the number of vertices.

        Returns:
            Tuple containing the mapping of vertex to its component, the list
            of component sizes, and the initial number of components.
        """
        vertex_to_component = {vertex: vertex for vertex in self.vertices}
        component_sizes = [1] * len(self.vertices)
        num_components = len(self.vertices)
        return vertex_to_component, component_sizes, num_components

    def perform_iteration(
        self,
        vertex_to_component: Dict[int, int],
        component_sizes: List[int],
        num_components: int,
        mst_edges: List[Tuple[int, int, int]],
        mst_weight: int,
    ):
        """
        Perform one iteration of Boruvka's algorithm, finding the minimum
        connecting edge for each component and connecting components using
        these edges.

        Args:
            vertex_to_component: Mapping of vertices to their component.
            component_sizes: List containing the sizes of each component.
            num_components: Total number of components in the graph.
            mst_edges: List of edges in the minimum spanning tree so far.
            mst_weight: Total weight of the minimum spanning tree so far.

        Returns:
            Tuple containing the updated MST weight and number of components.
        """
        # Initialize list to store minimum connecting edge for each component.
        min_connecting_edge_per_component = [None] * len(self.vertices)
        # Update the minimum connecting edge for each component.
        self.update_min_edge_per_component(
            vertex_to_component, min_connecting_edge_per_component
        )
        # Connect components using the minimum connecting edges and update MST
        # weight and number of components.
        mst_weight, num_components = self.connect_components_with_min_edges(
            component_sizes,
            min_connecting_edge_per_component,
            mst_edges,
            mst_weight,
            vertex_to_component,
            num_components,
        )

        return mst_weight, num_components

    def draw_mst(self, mst_edges: List[Tuple[int, int, int]]) -> None:
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
            vertex1, vertex2, weight = edge
            G.add_edge(vertex1, vertex2, weight=weight)
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
        (
            vertex_to_component,
            component_sizes,
            num_components,
        ) = self.initialize_components()
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
                vertex_to_component,
                component_sizes,
                num_components,
                mst_edges,
                mst_weight,
            )

        # Summarise the MST found and draw it.
        print("\nMST found with Boruvka's algorithm.")
        print("MST edges (vertex_1, vertex_2, weight):")
        for edge in sorted(mst_edges):
            print(f"    {edge}")
        print(f"MST weight: {mst_weight}")
        self.draw_mst(mst_edges)

        return mst_weight, mst_edges


def main():
    """
    Run Boruvka's algorithm on an example graph.
    """
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
    graph1.run_boruvkas_algorithm()


if __name__ == "__main__":
    main()
