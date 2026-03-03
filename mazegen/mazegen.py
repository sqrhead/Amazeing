import random
from typing import Optional

# Coords
WEST: int = 8
SOUTH: int = 4
EAST: int = 2
NORTH: int = 1

#  Coord to usable Directions
DIRECTIONS: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0)
}

# Direction to Coords
RDIRECTIONS: dict[tuple[int, int], int] = {
    (0, -1): NORTH,
    (0, 1): SOUTH,
    (1, 0): EAST,
    (-1, 0): WEST
}

# Opposites
OPPOSITES: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}


class MazeGenerator:
    """
    Generates a maze using recursive backtracking algorithm.

    The maze is represented as a 2D grid where each cell stores its
    wall state as a 4-bit integer (N=1, E=2, S=4, W=8). A bit set to
    1 means the wall is closed, 0 means open.
    A '42' pattern is embedded at the center of the maze using fully
    walled cells that are excluded from the generation process.

    Attributes:
        width: The width of the maze
        height: The height of the maze
        grid: 2D list with wall state of each cell
        visited: 2D list tracking which cells have been visited by DFS
        pattern_cells: List of (x, y) coordinates belonging to 42 pattern
        entry: Coordinates of the maze entry point
        exit: Coordinates of the maze exit point

    """
    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            seed: Optional[int] = 42) -> None:
        """
        Initialize the maze grid, visited array and 42 pattern.

            Args:
                width: Number of cells horizontally.
                height: Number of cells vertically.
                entry: (x, y) coordinates of the maze entry point.
                exit: (x, y) coordinates of the maze exit point.
                seed: Random seed for reproducibility. Defaults to 42.
        """
        random.seed(seed)
        self.width = width
        self.height = height
        self.sym_min_size = 9  # const var
        self.grid: list[list[int]] = []
        self.visited: list[list[bool]] = []
        self.pattern_cells: list[tuple[int, int]] = []

        self.entry = entry
        self.exit = exit
        # Grid setup
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                self.grid[y].append(WEST | SOUTH | EAST | NORTH)

        # Grid visited setup
        for y in range(self.height):
            self.visited.append([])
            for x in range(self.width):
                self.visited[y].append(False)

        # Carve 42 Pattern
        self.pattern = [
            [1, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1],
        ]
        self.start_x = (self.width - len(self.pattern[0])) // 2
        self.start_y = (self.height - len(self.pattern)) // 2

        if self.width <= self.sym_min_size or self.height <= self.sym_min_size:
            print("[INFO]: 42Pattern too big to fit in the maze")
            return
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == 1:
                    self.visited[self.start_y + y][self.start_x + x] = True
                    self.pattern_cells.append(
                        (self.start_x + x, self.start_y + y)
                    )

    def _is_inside_pattern(self, x: int, y: int) -> bool:
        """Check if coordinates belong to the 42 pattern.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if the cell is part of the pattern, False otherwise.
        """
        if (x, y) in self.pattern_cells:
            return True
        return False

    def _remove_wall(self, x: int, y: int, dir: int) -> None:
        """
        Remove the wall between a cell and its neighbor in a given direction.

        Updates both the cell and its neighbor to keep the grid coherent.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
            dir: Direction of the wall to remove (NORTH, SOUTH, EAST or WEST).
        """
        self.grid[y][x] &= ~dir
        dx, dy = DIRECTIONS[dir]
        nx, ny = x + dx, y + dy
        self.grid[ny][nx] &= ~OPPOSITES[dir]

    def _get_neighbors(self, x: int, y: int) -> list[
            tuple[int, int, int]
            ]:
        """Get all unvisited valid neighbors of a cell.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.

        Returns:
            List of tuples (nx, ny, direction) for each unvisited neighbor,
            where direction is the wall direction to remove to reach it.
        """
        neighbors: list[tuple[int, int, int]] = []

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            try:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= self.width:
                    continue
                if ny < 0 or ny >= self.height:
                    continue

                if self.visited[y + dy][x + dx] is False:
                    neighbors.append((x + dx, y + dy, RDIRECTIONS[(dx, dy)]))

            except Exception:
                continue

        return neighbors

    def _unperfect(self) -> None:
        """Create loops in the maze by randomly removing extra walls.

        Called after generation to turn a perfect maze into an imperfect
        one with multiple possible paths. Skips border cells, pattern
        cells, and the entry/exit points.
        """
        target = self.width * self.height // 10 + self.width
        counter = 0
        rnd_dirs = [8, 4, 2, 1]
        while counter <= target:
            rnd_x = random.randint(1, self.width - 2)
            rnd_y = random.randint(1, self.height - 2)
            rnd_dir = rnd_dirs[random.randint(0, len(rnd_dirs) - 1)]
            dx, dy = DIRECTIONS[rnd_dir]
            nx, ny = rnd_x + dx, rnd_y + dy
            if self._is_inside_pattern(rnd_x, rnd_y) is False and \
                not self._is_inside_pattern(nx, ny) and \
                1 <= nx <= self.width - 2 and \
                1 <= ny <= self.height - 2 and \
                    self.entry != (rnd_x, rnd_y) and \
                    self.exit != (rnd_x, rnd_y):

                self._remove_wall(rnd_x, rnd_y, rnd_dir)
                counter += 1

    def generate(self, perfect: bool = True) -> list[list[int]]:
        """Generate the maze using recursive backtracking (DFS).

        Args:
            perfect: If True, generates a perfect maze with exactly one
                     path between any two cells. If False, calls
                     _unperfect() to add extra passages.

        Returns:
            2D list of integers encoding wall states per cell.
        """

        start_point_x: int = random.randint(1, self.width - 1)
        start_point_y: int = random.randint(1, self.height - 1)
        # Stack of path
        stack: list[tuple[int, int]] = [(start_point_x, start_point_y)]
        # Visited cells so we dont need to go there again
        self.visited[start_point_y][start_point_x] = True

        while stack:
            x, y = stack[-1]
            neighbors = self._get_neighbors(x, y)

            if neighbors:
                new_dir = neighbors[random.randint(0, len(neighbors) - 1)]
                if new_dir:
                    self._remove_wall(x, y, new_dir[2])
                self.visited[new_dir[1]][new_dir[0]] = True
                stack.append((new_dir[0], new_dir[1]))
            else:
                stack.pop()

        for x in range(self.width):
            self.grid[0][x] |= NORTH
            self.grid[self.height-1][x] |= SOUTH
        for y in range(self.height):
            self.grid[y][0] |= WEST
            self.grid[y][self.width - 1] |= EAST

        if not perfect:
            self._unperfect()

        return self.grid
