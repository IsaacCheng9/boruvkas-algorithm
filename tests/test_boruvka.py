import pytest

from boruvkas_algorithm.boruvka import Graph, find_mst_with_boruvkas_algorithm
from boruvkas_algorithm.union_find import UnionFind


@pytest.fixture
def setup_graph():
    """
    Fixture to create a graph instance for testing.

    Returns:
        An instance of the Graph class initialized with a predetermined number
        of vertices.
    """
    return Graph(9)  # Example graph with 9 vertices.


def test_graph_initialization():
    """
    Tests that a graph is initialised with the correct number of vertices and
    no edges.
    """
    graph = Graph(5)
    assert len(graph.vertices) == 5, "Graph should have 5 vertices"
    assert len(graph.edges) == 0, "Graph should be initialised with no edges"


def test_add_edge(setup_graph: Graph):
    """
    Tests that edges are correctly added by checking the length of the edge
    list after addition.
    """
    graph = setup_graph
    graph.add_edge(0, 1, 4)
    assert len(graph.edges) == 1, "Edge should be added to the graph"


def test_add_edge_invalid_vertices(setup_graph: Graph):
    """
    Tests the addition of an edge with non-existing vertices.

    Expects a ValueError to be raised when trying to add an edge with at least
    one non-existing node.
    """
    graph = setup_graph
    with pytest.raises(ValueError):
        # Use node indices that do not exist in the graph.
        graph.add_edge(10, 11, 5)


# =============================================================================
# UnionFind Tests
# =============================================================================


def test_union_find_initialization():
    """Tests that UnionFind initialises with correct parent and rank arrays."""
    uf = UnionFind(5)
    assert uf.parent == [0, 1, 2, 3, 4], "Each node should be its own parent"
    assert uf.rank == [1, 1, 1, 1, 1], "Each node should have rank 1"


def test_union_find_find_single_node():
    """Tests that find returns the node itself when it's its own parent."""
    uf = UnionFind(5)
    assert uf.find(0) == 0
    assert uf.find(4) == 4


def test_union_find_union_two_nodes():
    """Tests that union correctly combines two nodes."""
    uf = UnionFind(5)
    result = uf.union(0, 1)
    assert result is True, "Union should return True when nodes are combined"
    assert uf.find(0) == uf.find(1), "Nodes should have the same root after union"


def test_union_find_union_already_connected():
    """Tests that union returns False when nodes are already connected."""
    uf = UnionFind(5)
    uf.union(0, 1)
    result = uf.union(0, 1)
    assert result is False, "Union should return False when already connected"


def test_union_find_union_by_size():
    """Tests that smaller trees are merged into larger trees."""
    uf = UnionFind(5)
    # Create a larger tree: 0 <- 1, 0 <- 2
    uf.union(0, 1)
    uf.union(0, 2)
    # Now union with node 3 - node 3 should be merged into the larger tree.
    uf.union(3, 0)
    # The root of the larger tree should remain the root.
    root = uf.find(0)
    assert uf.find(3) == root, "Smaller tree should be merged into larger tree"


def test_union_find_path_compression():
    """Tests that path compression flattens the tree structure."""
    uf = UnionFind(5)
    # Create a chain: 0 <- 1 <- 2 <- 3
    uf.parent = [0, 0, 1, 2, 4]
    uf.rank = [4, 1, 1, 1, 1]
    # Find on node 3 should compress the path.
    root = uf.find(3)
    assert root == 0, "Root should be 0"
    # After path compression, intermediate nodes should point closer to root.
    assert uf.parent[2] in (0, 1), "Path compression should shorten the path"


def test_union_find_multiple_components():
    """Tests UnionFind with multiple separate components."""
    uf = UnionFind(6)
    # Create two components: {0, 1, 2} and {3, 4, 5}
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(4, 5)

    # Check components are separate.
    assert uf.find(0) == uf.find(1) == uf.find(2)
    assert uf.find(3) == uf.find(4) == uf.find(5)
    assert uf.find(0) != uf.find(3), "Components should be separate"

    # Merge the two components.
    uf.union(2, 3)
    assert uf.find(0) == uf.find(5), "Components should be merged"


def test_union_find_is_connected():
    """Tests the is_connected convenience method."""
    uf = UnionFind(5)
    assert not uf.is_connected(0, 1), "Nodes should not be connected initially"

    uf.union(0, 1)
    assert uf.is_connected(0, 1), "Nodes should be connected after union"
    assert not uf.is_connected(0, 2), "Unconnected nodes should return False"

    uf.union(1, 2)
    assert uf.is_connected(0, 2), "Transitively connected nodes should return True"


# =============================================================================
# MST Algorithm Tests
# =============================================================================


def test_mst_with_injected_union_find(setup_graph: Graph):
    """Tests that the algorithm works with an injected UnionFind instance."""
    graph = setup_graph
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

    # Inject a custom UnionFind instance.
    union_find = UnionFind(len(graph.vertices))
    mst_weight, mst_edges = find_mst_with_boruvkas_algorithm(graph, union_find)

    assert mst_weight == 29, "MST weight should be 29"
    assert len(mst_edges) == 8, "MST should have 8 edges for 9 vertices"


def test_mst(setup_graph: Graph):
    """
    Tests that the MST has the correct total weight and structure by comparing
    to known MST values for a predefined graph.
    """
    graph = setup_graph
    # Add edges to setup_graph fixture to form a specific connected graph.
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

    mst_weight, mst_edges = find_mst_with_boruvkas_algorithm(graph)
    expected_weight = 29
    expected_edges = [
        (0, 1, 4),
        (0, 6, 7),
        (2, 3, 6),
        (2, 4, 2),
        (3, 5, 5),
        (4, 7, 1),
        (6, 7, 1),
        (7, 8, 3),
    ]

    assert mst_weight == expected_weight, "MST weight does not match expected value"
    assert sorted(mst_edges) == sorted(expected_edges), (
        "MST edges do not match expected edges"
    )


def test_mst_simple_triangle():
    """Tests MST on a simple triangle graph."""
    graph = Graph(3)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 2)
    graph.add_edge(0, 2, 3)

    mst_weight, mst_edges = find_mst_with_boruvkas_algorithm(graph)

    assert mst_weight == 3, "MST weight should be 3 (edges 1 + 2)"
    assert len(mst_edges) == 2, "MST should have 2 edges for 3 vertices"


def test_mst_linear_graph():
    """Tests MST on a linear graph (already a tree)."""
    graph = Graph(4)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 2)
    graph.add_edge(2, 3, 3)

    mst_weight, mst_edges = find_mst_with_boruvkas_algorithm(graph)

    assert mst_weight == 6, "MST weight should be 6 (1 + 2 + 3)"
    assert len(mst_edges) == 3, "MST should have 3 edges for 4 vertices"
