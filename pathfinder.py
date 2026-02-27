from cell import Cell
from collections import deque

# BFS algorithm for pathfinding
'''
The pathfinder  moves from start cell
until end cell is reached
ing all neighbors of every curr cell we are on
putting them on visited stack.

After we reach end cell, we need the to backtrack on the cells
we go form end and look for his parent until we reach start.

For this reason a PathfinderNode class was created to ensure a better way to do it
'''

class PathfinderNode:
    def __init__(self, node: Cell, parent: Cell):
        self.node = node
        self.parent = parent


class Pathfinder:
    def __init__(self, maze: list[Cell]):
        self.maze = maze

    def get_cell(self, x: int, y: int) -> Cell:
        for cell in self.maze:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor is not None and neighbor.type == 1:
                neighbors.append(neighbor)

        return neighbors


    def find_closer(self, cell: Cell, end: Cell) -> Cell:
        neighbors = self.get_neighbors(cell, self.maze)
        print(f"n_neighbors: {len(neighbors)}")
        distance: float = self.get_distance(cell, end)
        print(f"distance: {distance}")
        closer_cell: Cell = cell
        for i in neighbors:
            new_distance = self.get_distance(i, end)
            if new_distance < distance:
                closer_cell = i
                distance = new_distance
        return closer_cell

    def get_path(self, start: Cell, end: Cell) -> list[Cell]:
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