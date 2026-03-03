from __future__ import annotations
from collections import deque
from typing import Optional

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

DIRECTIONS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}


class PathfinderNode:
    """Represents a single node in the BFS pathfinding tree.

    Each node stores its coordinates and a reference to its parent,
    allowing the shortest path to be retraced from end to start.

    Attributes:
        x: Column index of the node.
        y: Row index of the node.
        parent: The node from which this node was reached, or None
                if this is the start node.
    """
    def __init__(
            self,
            x: int,
            y: int,
            parent: Optional[PathfinderNode] = None
            ) -> None:
        """Initialize a pathfinder node.

        Args:
            x: Column index.
            y: Row index.
            parent: Parent node in the BFS tree. Defaults to None.
        """
        self.x = x
        self.y = y
        self.parent: Optional[PathfinderNode] = parent

    def equal(self, other_x: int, other_y: int) -> bool:
        """Check if this node matches the given coordinates.

        Args:
            other_x: Column index to compare.
            other_y: Row index to compare.

        Returns:
            True if coordinates match, False otherwise.
        """
        if self.x == other_x and self.y == other_y:
            return True
        return False


class Pathfinder:
    """Finds the shortest path in a maze using Breadth First Search (BFS).

    Traverses the maze grid by checking wall bits to determine which
    directions are passable, then retraces the shortest path from
    end to start using PathfinderNode parent references.

    Attributes:
        grid: 2D list encoding wall states per cell as integers.
    """
    def __init__(self, grid: list[list[int]]) -> None:
        """Initialize the pathfinder with a maze grid.

        Args:
            grid: 2D list of integers encoding wall states per cell.
        """
        self.grid = grid

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Get all accessible neighbors of a cell based on wall states.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.

        Returns:
            List of (x, y) coordinates of reachable neighboring cells.
        """
        neighbors: list[tuple[int, int]] = []

        for dir, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < len(self.grid[0]) and \
                    ny >= 0 and ny < len(self.grid):
                if not (self.grid[y][x] & dir):
                    neighbors.append((nx, ny))
        return neighbors

    def get_path(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
            ) -> list[tuple[int, int]]:
        """Find the shortest path between two cells using BFS.

        Args:
            start: (x, y) coordinates of the starting cell.
            end: (x, y) coordinates of the destination cell.

        Returns:
            List of (x, y) coordinates from start to end representing
            the shortest path. Returns an empty list if no path exists.
        """
        pn_start: PathfinderNode = PathfinderNode(start[0], start[1], None)

        que = deque([pn_start])
        visited = [start]

        while que:
            curr = que.popleft()

            if curr.equal(end[0], end[1]):
                path = []
                node: Optional[PathfinderNode] = curr
                while node is not None:
                    path.append((node.x, node.y))
                    node = node.parent
                path.reverse()
                return path

            for nx, ny in self.get_neighbors(curr.x, curr.y):
                if (nx, ny) not in visited:
                    visited.append((nx, ny))
                    pn_neighbor = PathfinderNode(nx, ny, curr)
                    que.append(pn_neighbor)
        return []
