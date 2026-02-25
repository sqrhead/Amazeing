from cell import Cell
import math

class Pathfinder:
    def __init__(self, maze: list[Cell]):
        self.maze = maze

    def get_cell(self, x: int, y: int) -> Cell:
        for cell in self.maze:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def get_neighbors(self, cell, maze) -> list[Cell]:
        neighbors: list[Cell] = []
        for x in [-1, 1]:
            new_c = self.get_cell(cell.x + x, cell.y)
            if new_c.type == 1:
                neighbors.append(new_c)

        for y in [-1, 1]:
            new_c = self.get_cell(cell.x, cell.y + y)
            if new_c.type == 1:
                neighbors.append(new_c)

        return neighbors


    def get_distance(self, cell: Cell, cell2: Cell) -> float:
        return float(math.sqrt((cell2.x - cell.x)**2 + (cell2.y -cell.y)**2))

    def find_closer(self, cell: Cell, end: Cell) -> Cell:
        neighbors = self.get_neighbors(cell, self.maze)
        closer: float = self.get_distance(cell, end)
        closer_cell: Cell = cell
        for i in neighbors:
            if self.get_distance(closer_cell, end) < closer:
                closer_cell = i
        return closer_cell

    def get_path(self, start: Cell, end: Cell) -> list[Cell]:
        if start.type != 1:
            raise SystemExit("[Error]: Pathfinder start cell not valid")
        if end.type != 1:
            raise SystemExit("[Error]: Pathfinder end cell not valid")

        curr_cell: Cell = start
        path: list[Cell] = []
        path.append(start)
        while curr_cell is not end:
            print(f"curr_cell: {curr_cell.x}, {curr_cell.y}")
            curr_cell = self.find_closer(curr_cell, end)
            path.append(curr_cell)

        return path
