class UnionFind:
    """
    Union-find (disjoint set union) data structure for tracking connected
    components with path compression and union by size.
    """

    def __init__(self, size: int) -> None:
        """
        Initialises the Union-Find structure.

        Args:
            size: The number of elements in the structure.
        """
        # Each node is its own parent initially.
        self.parent: list[int] = list(range(size))
        # Each tree has size 1 (itself) initially.
        self.rank: list[int] = [1] * size

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
        # If they have the same root parent, they're already connected.
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

    def is_connected(self, node1: int, node2: int) -> bool:
        """
        Checks if two nodes are in the same component.

        Args:
            node1: The first node.
            node2: The second node.

        Returns:
            True if the nodes are connected, False otherwise.
        """
        return self.find(node1) == self.find(node2)
