"""
Implement Boruvka's algorithm for finding the minimum spanning tree of a graph.
"""
from typing import List, Tuple


class Graph:
    def __init__(self, num_nodes: int):
        """
        Args:
            num_nodes: The number of nodes to generate in the graph.
        """
        self.num_nodes = num_nodes
        self.nodes = [node for node in range(num_nodes)]
        # [(node1, node2, weight)]
        self.edges = []
        # {node: parent} to represent the component trees. Initially, each node
        # is its own parent, as the graph is disconnected.
        self.components = {node: node for node in self.nodes}

    def get_nodes(self) -> list:
        """
        Return a list of nodes in this graph.
        """
        return self.nodes

    def get_edges(self) -> List[tuple]:
        """
        Return a list of edges in this graph.
        """
        return self.edges

    def add_edge(self, node1: int, node2: int, weight: int) -> bool:
        """
        Add an edge to this graph from node1 to node2 with a given weight.

        Args:
            node1: The first node to connect the edge with.
            node2: The second node to connect the edge with.
            weight: The weight of the edge to add.

        Raises:
            ValueError: When either node1 or node2 do not exist in this graph.

        Returns:
            True if the edge was added successfully.
        """
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} does not exist")
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} does not exist")

        self.edges.append((node1, node2, weight))
        return True

    def merge_components(
        self, component_size: List[int], node1: int, node2: int
    ) -> None:
        """
        Merge the smaller component of node1 and node2 into the larger
        component.

        Args:
            component_size: A list of the size of each component.
            node1: The first node to merge the component of.
            node2: The second node to merge the component of.
        """
        node1_component = self.components[node1]
        node2_component = self.components[node2]

        # Merge the smaller component into the larger component.
        if component_size[node1_component] < component_size[node2_component]:
            self.components[node1_component] = node2_component
            component_size[node2_component] += component_size[node1_component]
        else:
            self.components[node2_component] = node1_component
            component_size[node1_component] += component_size[node2_component]

    def update_min_weight_edge_for_components(self, min_weight_edges, edge):
        """
        Update the minimum weight edge if the given edge is the smallest so far
        for either of the nodes' components.

        Args:
            min_weight_edges: A list of the minimum weight edge for each node's
                              component.
            edge: The edge to check, in the form (node1, node2, weight).
        """
        node1, node2, weight = edge
        node1_component = self.components[node1]
        node2_component = self.components[node2]

        if node1_component != node2_component:
            if (
                min_weight_edges[node1_component] == -1
                or weight < min_weight_edges[node1_component][2]
            ):
                min_weight_edges[node1_component] = edge

            if (
                min_weight_edges[node2_component] == -1
                or weight < min_weight_edges[node2_component][2]
            ):
                min_weight_edges[node2_component] = edge

    def find_mst_with_boruvka(self) -> Tuple[int, List[tuple]]:
        """
        Find the minimum spanning tree of this graph using Boruvka's algorithm.

        Returns:
            The weight and list of edges of the minimum spanning tree.
        """
        print(
            "\nFinding MST with Boruvka's algorithm for the following graph:\n"
            f"Nodes: {self.nodes}\nEdges (node1, node2, weight):\n    {self.edges}\n"
        )
        mst_weight = 0
        mst_edges = []
        # Initially, each node is its own component as the graph is
        # disconnected.
        component_size = [1] * self.num_nodes
        num_of_components = self.num_nodes

        # Continue adding edges until there is only one component, as this
        # means the graph is connected.
        while num_of_components > 1:
            # Reset the min_weight_edge list to find the next minimum weight.
            min_weight_edges = [-1] * self.num_nodes
            # Find the minimum weight edge for each component, so we have the
            # optimal candidate edges to add to the MST.
            for edge in self.edges:
                self.update_min_weight_edge_for_components(min_weight_edges, edge)

            for node in self.nodes:
                # If the node isn't in a component, skip it.
                if min_weight_edges[node] == -1:
                    continue

                node1, node2, weight = min_weight_edges[node]
                # If the other node isn't in the same component, connect and
                # merge them in the MST using the minimum weight edge.
                if self.components[node1] != self.components[node2]:
                    self.merge_components(component_size, node1, node2)
                    mst_weight += weight
                    mst_edges.append((node1, node2, weight))
                    # We have one less component as we've merged two.
                    num_of_components -= 1
                    print(f"Added edge {node1} - {node2} with weight {weight} to MST.")

        print("Successfully found MST with Boruvka's algorithm.")
        return mst_weight, mst_edges


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
    mst_weight, mst_edges = graph1.find_mst_with_boruvka()
    print(f"\nMST weight: {mst_weight}")
    print(f"MST edges (node1, node2, weight):\n    {mst_edges}\n")


if __name__ == "__main__":
    main()
