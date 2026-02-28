import random
from pathfinder import Pathfinder

# --------------------------------------------------------------------#
#                            GLOBAL DATA
# --------------------------------------------------------------------#
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
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.sym_min_size = 8
        self.grid: list[list[int]] = []

        self.visited: list[list[bool]]= []

        # Grid setup
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                self.grid[y].append(8 | 4 | 2 | 1)


        # Grid visited setup
        for y in range(self.height):
            self.visited.append([])
            for x in range(self.width):
                self.visited[y].append(False)


        # Carve 42 Pattern
        self.pattern = [
            [99,0,0,0,99,99,99],
            [99,0,99,0,0,0,99],
            [99,99,99,0,99,99,99],
            [0,0,99,0,99,0,0],
            [0,0,99,0,99,99,99],
        ]
        start_x = (self.width - len(self.pattern[0])) // 2
        start_y = (self.height - len(self.pattern)) // 2

        # Control to check if self.pattern is too big to fit in the maze
        if self.width <= self.sym_min_size or self.height <= self.sym_min_size:
            print("[INFO]: 42Pattern too big to fit in the maze")
            return
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == 99:
                    self.grid[start_y + y][start_x + x] = self.pattern[y][x]
                    self.visited[start_y + y][start_x + x] = True
                else:
                    self.grid[start_y + y][start_x + x] = 15


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

        ...
    # Params:  entry_x,entry_y start point to carv
    def generate(self) -> None:

        stack: list[tuple[int, int]] = [(0, 0)]
        self.visited[0][0] = True

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
        PATH = "\033[1;55m██\033[0m"

        pathfinder: Pathfinder = Pathfinder(self.grid)
        path = pathfinder.get_path(sx, sy, ex, ey)

        for y in range(self.height):
            top = ""
            mid = ""
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell == 99:
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
            end_cap = SYMB if self.grid[y][self.width-1] == 99 else WALL
            print(top + end_cap)
            print(mid + end_cap)

        # Close bottom
        print(WALL * (self.width * 2 + 1))


# [BUG] With size (10, 7) sometimes the pattern is modified, and creating loops too
if __name__ == "__main__":

    mg: MazeGenerator = MazeGenerator(50, 25)

    # TODO: Return the maze array
    mg.generate()
    mg.display(2, 2, mg.width - 1, mg.height -1)
    ...