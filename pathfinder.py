from cell import Cell


# BFS algorithm for pathfinding
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
            if neighbor.type == 1 and neighbor is not None:
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
        if start.type != 1:
            raise SystemExit("[Error]: Pathfinder start cell not valid")
        if end.type != 1:
            raise SystemExit("[Error]: Pathfinder end cell not valid")

        path: list[Cell] = []
        stack: list[Cell] = [start]
        visited: list[Cell] = []

        while len(stack) > 0:
            path.append(stack.pop())
            curr_cell = path[-1]

            if curr_cell is end:
                return path

            for neighbor in self.get_neighbors(curr_cell):
                if neighbor not in visited:
                    visited.append(neighbor)
                    stack.append(neighbor)
        return []