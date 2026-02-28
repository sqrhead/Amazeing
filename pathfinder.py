from __future__ import annotations
from collections import deque
'''
***** Class PathfinderNode ************************************************************************
-- For this pathfinding algorithm we need to retrace backwards
-- The way we did this is by PathfinderNodes, it has current coords, and parent coords
***************************************************************************************************

***** Class Pathfinding ***************************************************************************
-- The idea is to travel from start coords until we find end coords
-- The problem is we add to the 'path' too many useless coords
-- So we use the PathfinderNodes to start from end and retrace everything
-- The name Breadth First Search is the name of the algorithm if you want to find more about it
***************************************************************************************************
'''
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

DIRECTIONS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}

class PathfinderNode:
    def __init__(self, x: int, y: int, parent: PathfinderNode = None):
        self.x = x
        self.y = y
        self.parent: PathfinderNode = parent

    def equal(self, other_x: int, other_y: int) -> bool:
        if self.x == other_x and self.y == other_y:
            return True
        return False

class Pathfinder:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []

        for dir, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < len(self.grid[0]) and ny >= 0 and ny < len(self.grid):
                if not (self.grid[y][x] & dir):
                    neighbors.append((nx, ny))
        return neighbors


    def get_path(self, sx: int, sy: int, ex: int, ey: int) -> list[tuple[int, int]]:
        pn_start: PathfinderNode = PathfinderNode(sx, sy)

        que = deque([pn_start])
        visited = [(sx, sy)]

        while que:
            curr = que.popleft()

            if curr.equal(ex, ey):
                path = []
                node = curr
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

