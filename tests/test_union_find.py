from boruvkas_algorithm.boruvka import UnionFind


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


def test_union_find_connected():
    """Tests the connected convenience method."""
    uf = UnionFind(5)
    assert not uf.is_connected(0, 1), "Nodes should not be connected initially"

    uf.union(0, 1)
    assert uf.is_connected(0, 1), "Nodes should be connected after union"
    assert not uf.is_connected(0, 2), "Unconnected nodes should return False"

    uf.union(1, 2)
    assert uf.is_connected(0, 2), "Transitively connected nodes should return True"
