import random

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
        pattern = [
            [99,0,0,0,99,99,99],
            [99,0,99,0,0,0,99],
            [99,99,99,0,99,99,99],
            [0,0,99,0,99,0,0],
            [0,0,99,0,99,99,99],
        ]
        start_x = (self.width - len(pattern[0])) // 2
        start_y = (self.height - len(pattern)) // 2

        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                if pattern[y][x] == 99:
                    self.grid[start_y + y][start_x + x] = pattern[y][x]
                    self.visited[start_y + y][start_x + x] = True
                else:
                    self.grid[start_y + y][start_x + x] = 15


    # Params: x for row, y for col and dir for [NORTH, SOUTH, EAST, WEST]
    def remove_wall(self, x: int, y: int, dir: int) -> None:
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
    def generate(self, entry_x: int, entry_y: int) -> None:

        stack: list[tuple[int, int]] = [(entry_x, entry_y)]
        self.visited[entry_y][entry_x] = True

        while stack:
            x, y = stack[-1]
            neighbors = self._get_neighbors(x, y)

            if neighbors:
                new_dir = neighbors[random.randint(0, len(neighbors) -1)]
                if new_dir:
                    self.remove_wall(x, y, new_dir[2]) # [2] is the direction got from RDIRECTIONS
                self.visited[new_dir[1]][new_dir[0]] = True
                stack.append(( new_dir[0],new_dir[1]))
            else:
                stack.pop()

    def display(self) -> None:

        for y in range(self.height):
            # Draw top side
            for x in range(self.width):
                if self.grid[y][x] == 99:
                    # print("\033[0;32m+##\033[00m", end="")
                    print("+##", end="")
                elif self.grid[y][x] & NORTH:
                    print("+--", end="")
                else:
                    print("+  ", end="")
            print("+")
            # Draw west side
            for x in range(self.width):
                if self.grid[y][x] == 99:
                    # print("\033[0;32m+##\033[00m", end="")
                    print("+##", end="")
                elif self.grid[y][x] & WEST:
                    print("|  ", end="")
                else:
                    print("   ", end="")
            print("|")

        # Draw bottom line
        for x in range(self.width):
            print("+--", end="")
        print("+")


    def display_blk(self) -> None:
        WALL  = "\033[33m██\033[0m"   # Yellow wall
        FLOOR = "  "                   # Passage (2 spaces)
        SYMB  = "\033[32m██\033[0m"   # Green pattern

        for y in range(self.height):
            top = ""
            mid = ""
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell == 99:
                    # If it's the pattern, both the 'wall' space
                    # and the 'cell' space are green blocks.
                    top += SYMB + SYMB
                    mid += SYMB + SYMB
                else:
                    # 1. TOP ROW (The North Wall)
                    # Every cell needs a corner pillar first
                    top += WALL
                    # Then the actual North wall or a gap
                    top += WALL if (cell & NORTH) else FLOOR

                    # 2. MIDDLE ROW (The West Wall)
                    # The West wall or a gap
                    mid += WALL if (cell & WEST) else FLOOR
                    # The walkable center of the cell
                    mid += FLOOR

            # Print the rows and close the right-hand side with a final wall
            # We check the last cell of the row for the pattern to keep the border clean
            end_cap = SYMB if self.grid[y][self.width-1] == 99 else WALL
            print(top + end_cap)
            print(mid + end_cap)

        # 3. BOTTOM BORDER
        # Total width is (2 characters per cell) + 1 for the final end cap
        print(WALL * (self.width * 2 + 1))




if __name__ == "__main__":

    mg: MazeGenerator = MazeGenerator(20, 15)

    # TODO: Return the maze array
    mg.generate(1,1)
    mg.display_blk()
    ...