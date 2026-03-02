import random
from typing import Optional
from time import sleep
from pathfinder import Pathfinder
from filehex import FileHex
from displayer import Displayer

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
    def __init__(self, width: int, height: int, seed: Optional[int] = 42):
        self.width = width # Width of the grid
        self.height = height # Height of the grid
        self.sym_min_size = 8 # Min size of the maze to print the SYMB
        random.seed(seed)
        self.grid: list[list[int]] = [] # The grid :>
        self.visited: list[list[bool]]= [] # Nested lists needed for the Recursive Backtracking
        self.pattern_cells: list[tuple[int, int]] = [] # Used to check if coords are inside pattern cells

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
                    self.grid[self.start_y + y][self.start_x + x] = 15 # switch to 15
                    self.visited[self.start_y + y][self.start_x + x] = True
                    self.pattern_cells.append((self.start_x + x, self.start_y + y))
                else:
                    self.grid[self.start_y + y][self.start_x + x] = 15

    # ************************ PROTECTED **************************************** #
    def _is_inside_pattern(self, x: int, y: int) -> bool:
        if (x, y) in self.pattern_cells:
            return True
        return False

    # 101010 42
    # 100010 34
    # 001000 34

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

    def _unperfect(self):
        for i in range(self.width // 10 + 1):
            self.visited[random.randint(1, self.height - 2)][random.randint(1, self.width - 2)] = True
        ...

    # ************************ PUBLIC **************************************** #
    # Params:  entry_x,entry_y start point to carv
    def generate(self, perfect: bool = True) -> None:

        # duh
        start_point_x: int = self.width // 2
        # duh 2
        start_point_y: int = self.height // 2
        # Stack of path
        stack: list[tuple[int, int]] = [(start_point_x,start_point_y)]
        # Visited cells so we dont need to go there again
        self.visited[start_point_y][start_point_x] = True
        if not perfect:
            self._unperfect()

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


    # To display the maze we display the WEST and NORTH wall of each grid cel
    # Then we hard corde the last left wall and the bottom tiles
    # We create 2 local string variables and add to them what we will print
    def display(self, sx: int, sy: int, ex: int, ey: int) -> None:
        WALL  = "\033[33m██\033[0m"
        FLOOR = "  "
        SYMB  = "\033[0;36m██\033[0m"
        ENTRY = "\033[32m██\033[0m"
        EXIT = "\033[1;31m██\033[0m"
        PATH = "\033[1;55m ■\033[0m"

        pathfinder: Pathfinder = Pathfinder(self.grid)
        path = pathfinder.get_path(sx, sy, ex, ey)
        # path = []
        for y in range(self.height):
            top = ""
            mid = ""
            for x in range(self.width):
                cell = self.grid[y][x]

                if self._is_inside_pattern(x, y):
                    top += SYMB + SYMB
                    mid += SYMB + SYMB
                else:
                    # Top left corner
                    top += WALL
                    # North cell
                    if (cell & NORTH):
                        top += WALL
                    elif (x, y -1) in path and (x, y) in path:
                        top += PATH
                    else:
                        top += FLOOR
                    # top += WALL if (cell & NORTH) else FLOOR

                    # West wall
                    if (cell & WEST):
                        mid += WALL
                    elif (x - 1, y) in path and (x, y) in path:
                        mid += PATH
                    else:
                        mid += FLOOR
                    # mid += WALL if (cell & WEST) else FLOOR

                    # Floor between walls
                    if y == sy and x == sx:
                        mid += ENTRY
                    elif y == ey and x == ex:
                        mid += EXIT
                    elif (x, y) in path:
                        mid += PATH
                    else:
                        mid += FLOOR

            # Right most wall/symb
            end_cap = ""
            if self._is_inside_pattern(y, self.width -1):
                end_cap += SYMB
            else:
                end_cap += WALL

            # end_cap = SYMB if self.grid[y][self.width-1] == 99 else WALL
            print(top + end_cap)
            print(mid + end_cap)

        # Close bottom
        print(WALL * (self.width * 2 + 1))


# [TODO] Fix 99 custom SYMB, its not a clean solution
# [BUG] With size (10, 7) sometimes the pattern is modified, and creating loops too
# [BUG] Hex file has false data on SYMB cells since they are forced as special (99)
if __name__ == "__main__":

    mg: MazeGenerator = MazeGenerator(40, 10, random.randint(1, 2**32))


    # TODO: Return the maze array
    mg.generate(True)
    mg.display(2, 2, 19, 9)

    pathfinder = Pathfinder(mg.grid)
    path = pathfinder.get_path(2, 2, 19, 9)
    # displayer: Displayer = Displayer(mg.grid, path, (2, 2), (19, 9))
    # displayer.display(True)

    flhex: FileHex = FileHex(mg.grid, path, 'output.txt')
    flhex.generate()
    ...