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
RDIRECTIONS: dict[tuple, int] = {
    (0, -1): NORTH,
    (0, 1): SOUTH,
    (1, 0): EAST,
    (-1, 0): WEST
}

# Opposites duh
OPPOSITES: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}


class MazeGenerator:
    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            seed: Optional[int] = 42) -> None:

        self.width = width # Width of the grid
        self.height = height # Height of the grid
        self.sym_min_size = 9 # const var
        random.seed(seed)
        self.grid: list[list[int]] = [] # The grid :>
        self.visited: list[list[bool]]= [] # Nested lists needed for the Recursive Backtracking
        self.pattern_cells: list[tuple[int, int]] = [] # Used to check if coords are inside pattern cells

        self.entry = entry
        self.exit = exit
        # Grid setup
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                self.grid[y].append(WEST| SOUTH | EAST | NORTH) # Bit assign of all coords


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

        # Control to check if self.pattern is too big to fit in the maze
        if self.width <= self.sym_min_size or self.height <= self.sym_min_size:
            print("[INFO]: 42Pattern too big to fit in the maze")
            return
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == 1:
                    self.visited[self.start_y + y][self.start_x + x] = True
                    self.pattern_cells.append((self.start_x + x, self.start_y + y))

    # ************************ PROTECTED **************************************** #
    def _is_inside_pattern(self, x: int, y: int) -> bool:
        if (x, y) in self.pattern_cells:
            return True
        return False

    # Params: x for row, y for col and dir for [NORTH, SOUTH, EAST, WEST]
    def _remove_wall(self, x: int, y: int, dir: int) -> None:
        self.grid[y][x] &= ~dir
        dx, dy = DIRECTIONS[dir]
        nx, ny = x + dx, y + dy
        self.grid[ny][nx] &= ~OPPOSITES[dir]

    def _get_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        neighbors: list[tuple[int, int]] = []

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            try:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= self.width:
                    continue
                if ny < 0 or ny >= self.height:
                    continue

                if self.visited[y + dy][x + dx] == False:
                    neighbors.append((x + dx, y + dy, RDIRECTIONS[(dx, dy)]))

            except Exception:
                continue

        return neighbors

    def _unperfect(self) -> None:
        # [TODO] In case once of the cell visited is start/end everything crashes
        target = self.width * self.height // 10 + 1
        counter = 0
        rnd_dirs = [8, 4, 2, 1]
        while counter <= target:
            rnd_x = random.randint(1, self.width - 2)
            rnd_y = random.randint(1, self.height - 2)
            rnd_dir = rnd_dirs[random.randint(0, len(rnd_dirs) -1)]
            dx, dy = DIRECTIONS[rnd_dir]
            nx, ny = rnd_x + dx, rnd_y + dy
            if self._is_inside_pattern(rnd_x, rnd_y) is False and \
                not self._is_inside_pattern(nx, ny) and \
                1 <= nx <= self.width - 2 and \
                1 <= ny <= self.height - 2 and \
                self.entry  != (rnd_x, rnd_y) and  self.exit != (rnd_x, rnd_y):

                self._remove_wall(rnd_x, rnd_y, rnd_dir)
                counter += 1

    # ************************ PUBLIC **************************************** #
    # Params:  entry_x,entry_y start point to carv
    def generate(self, perfect: bool = True) -> list[list[int]]:

        # duh
        start_point_x: int = self.width // 2
        # duh 2
        start_point_y: int = self.height // 2
        # Stack of path
        stack: list[tuple[int, int]] = [(start_point_x,start_point_y)]
        # Visited cells so we dont need to go there again
        self.visited[start_point_y][start_point_x] = True


        while stack:
            x, y = stack[-1]
            neighbors = self._get_neighbors(x, y)

            if neighbors:
                new_dir = neighbors[random.randint(0, len(neighbors) -1)]
                if new_dir:
                    self._remove_wall(x, y, new_dir[2]) # [2] is the direction got from RDIRECTIONS
                self.visited[new_dir[1]][new_dir[0]] = True
                stack.append(( new_dir[0],new_dir[1]))
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


# [BUG] With size (10, 7) sometimes the pattern is modified, and creating loops too
# [BUG] Hex file has false data on SYMB cells since they are forced as special (99)