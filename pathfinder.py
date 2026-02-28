from cell import Cell
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


class PathfinderNode:
    def __init__(self, x: int, y: int, px: int, py: int):
        self.x = x
        self.y = y
        self.px = px
        self.py = py


class Pathfinder:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor is not None and neighbor.type == 1:
                neighbors.append(neighbor)

        return neighbors


    def get_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        if start is None or start.type != 1:
            raise SystemExit("[Error]: Pathfinder start cell not valid")
        if end is None or end.type != 1:
            raise SystemExit("[Error]: Pathfinder end cell not valid")

        pn_start: PathfinderNode = PathfinderNode(start, None)

        que = deque([pn_start])
        visited = [(start.x, start.y)]

        while que:
            curr = que.popleft()

            if curr.node is end:
                path = []
                node = curr
                while node is not None:
                    path.append(node.node)
                    node = node.parent
                path.reverse()
                return path

            for neighbor in self.get_neighbors(curr.node):
                if (neighbor.x, neighbor.y) not in visited:
                    visited.append((neighbor.x, neighbor.y))
                    pn_neighbor = PathfinderNode(neighbor, curr)
                    que.append(pn_neighbor)
        return []