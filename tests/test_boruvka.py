import pytest

from boruvkas_algorithm.boruvka import (
    Graph,
    UnionFind,
    find_mst_with_boruvkas_algorithm,
)


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
