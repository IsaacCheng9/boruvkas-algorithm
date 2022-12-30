"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from typing import Dict, List, Tuple


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
        # [(vertex1, vertex2, weight)]
        self.edges = []

    def get_vertices(self) -> List[int]:
        """
        Return a list of vertices in this graph.
        """
        return self.vertices

    def get_edges(self) -> List[Tuple[int, int, int]]:
        """
        Return a list of edges in this graph in the form
        (vertex1, vertex2, weight).
        """
        return self.edges

    def add_edge(self, vertex1: int, vertex2: int, weight: int) -> bool:
        """
        Add an edge to this graph from vertex1 to vertex2 with a given weight.

        Args:
            vertex1: The first vertex to connect the edge with.
            vertex2: The second vertex to connect the edge with.
            weight: The weight of the edge to add.

        Raises:
            ValueError: When either vertex1 or vertex2 do not exist in this
                        graph.

        Returns:
            True if the edge was added successfully.
        """
        if vertex1 not in range(len(self.vertices)):
            raise ValueError(f"vertex {vertex1} does not exist")
        if vertex2 not in range(len(self.vertices)):
            raise ValueError(f"vertex {vertex2} does not exist")

        self.edges.append((vertex1, vertex2, weight))
        return True

    def print_graph_info(self) -> None:
        """
        Print the graph's vertices and edges.
        """
        print(f"Vertices: {self.vertices}")
        print("Edges (vertex1, vertex2, weight):")
        for edge in sorted(self.edges):
            print(f"    {edge}")

    def merge_components(
        self,
        components: Dict[int, int],
        component_sizes: List[int],
        vertex1: int,
        vertex2: int,
    ) -> None:
        """
        Merge the smaller component of vertex1 and vertex2 into the larger
        component.

        Args:
            components: A dictionary containing the component of each vertex.
            component_sizes: A list of the size of each component.
            vertex1: The first vertex to merge the component of.
            vertex2: The second vertex to merge the component of.
        """
        vertex1_component = components[vertex1]
        vertex2_component = components[vertex2]

        # Merge the smaller component into the larger component.
        if component_sizes[vertex1_component] < component_sizes[vertex2_component]:
            components[vertex1_component] = vertex2_component
            component_sizes[vertex2_component] += component_sizes[vertex1_component]
        else:
            components[vertex2_component] = vertex1_component
            component_sizes[vertex1_component] += component_sizes[vertex2_component]

    def update_shortest_edge_per_vertex(
        self, components: Dict[int, int], min_connecting_edge_per_vertex: List[int]
    ):
        """
        Check each edge and update the shortest edge for each vertex if it
        connects two components together.

        Args:
            components: A dictionary containing the component of each vertex.
            min_connecting_edge_per_vertex: A list with the shortest edge
                                                 for each vertex that connects
                                                 to a new component.
        """
        for edge in self.edges:
            vertex1, vertex2, weight = edge
            vertex1_component = components[vertex1]
            vertex2_component = components[vertex2]

            # If the vertices are in different components and the edge is smaller
            # than the current minimum weight edge for either component, update
            # them.
            if vertex1_component != vertex2_component:
                if (
                    min_connecting_edge_per_vertex[vertex1_component] == -1
                    or weight < min_connecting_edge_per_vertex[vertex1_component][2]
                ):
                    min_connecting_edge_per_vertex[vertex1_component] = edge

                if (
                    min_connecting_edge_per_vertex[vertex2_component] == -1
                    or weight < min_connecting_edge_per_vertex[vertex2_component][2]
                ):
                    min_connecting_edge_per_vertex[vertex2_component] = edge

    def connect_components_with_min_edges(
        self,
        component_sizes: List[int],
        min_connecting_edge_per_vertex: List[int],
        mst_edges: List[Tuple[int, int, int]],
        mst_weight: int,
        components: Dict[int, int],
        num_components: int,
    ) -> Tuple[int, int]:
        """
        Connect any components with the shortest edge between them to reduce
        the number of components.

        Args:
            components: A dictionary containing the component of each vertex.
            component_sizes: A list of the number of vertices in each
                             component.
            min_connecting_edge_per_vertex: A list with the shortest edge
                                                 for each vertex.
            mst_edges: A list of edges in the MST.
            mst_weight: The weight of the MST that is being built.
            num_components: The number of components in the graph.

        Returns:
            The weight of the MST and number of components in the graph.
        """
        for vertex in self.vertices:
            # If the vertex isn't in a component, skip it.
            if min_connecting_edge_per_vertex[vertex] == -1:
                continue

            vertex1, vertex2, weight = min_connecting_edge_per_vertex[vertex]
            # If the other vertex isn't in the same component, connect and
            # merge them in the MST using the shortest edge.
            if components[vertex1] != components[vertex2]:
                self.merge_components(components, component_sizes, vertex1, vertex2)
                mst_weight += weight
                mst_edges.append((vertex1, vertex2, weight))
                # We have one less component as we've merged two.
                num_components -= 1
                print(f"Added edge {vertex1} -- {vertex2} with weight {weight} to MST.")

        return mst_weight, num_components

    def find_mst_with_boruvka(self) -> Tuple[int, List[tuple]]:
        """
        Find the minimum spanning tree of this graph using Boruvka's algorithm.

        Returns:
            The weight and list of edges of the minimum spanning tree.
        """
        print("\nFinding MST with Boruvka's algorithm for the following graph:")
        self.print_graph_info()

        mst_weight = 0
        mst_edges = []
        # {vertex: parent} to represent the component trees. Initially, each
        # vertex is its own component as the graph is disconnected.
        components = {vertex: vertex for vertex in self.vertices}
        component_sizes = [1] * len(self.vertices)
        num_components = len(self.vertices)
        iteration_num = 1

        # Continue adding edges until there is only one component, as this
        # means the graph is connected.
        while num_components > 1:
            print(
                f"\nIteration {iteration_num}:\n"
                f"    Current MST (vertex1, vertex2, weight): {mst_edges}\n"
                f"    Current MST Weight: {mst_weight}"
            )
            # Reset the list to find the shortest edge of each vertex.
            min_connecting_edge_per_vertex = [-1] * len(self.vertices)
            # Find the shortest edge for each component, so we have the optimal
            # candidate edges to add to the MST.
            self.update_shortest_edge_per_vertex(
                components, min_connecting_edge_per_vertex
            )
            # Connect components where possible, and update the MST weight and
            # number of components accordingly so we can stop when the graph is
            # connected.
            mst_weight, num_components = self.connect_components_with_min_edges(
                component_sizes,
                min_connecting_edge_per_vertex,
                mst_edges,
                mst_weight,
                components,
                num_components,
            )
            iteration_num += 1

        print("\nSuccessfully found MST with Boruvka's algorithm.")
        print("MST edges (vertex1, vertex2, weight):")
        for edge in sorted(mst_edges):
            print(f"    {edge}")
        print(f"MST weight: {mst_weight}")

        return mst_weight, mst_edges


if __name__ == "__main__":
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
