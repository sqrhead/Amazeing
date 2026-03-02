from typing import Optional

class Displayer:
    def __init__(self, grid: list[list[int]], path: list[tuple[int, int]], start: tuple[int, int], end: tuple[int, int]):
        self.grid = grid
        self.path = path
        self.sx, self.sy = start
        self.ex, self.ey = end
        self.north_coord: int = 1
        self.west_coord: int = 8

    def display_on_file(self, file_name: str) -> None:

        ...

    def display(self, display_path: Optional[bool] = False) -> None:
        WALL  = "\033[33m██\033[0m"
        FLOOR = "  "
        SYMB  = "\033[0;36m██\033[0m"
        ENTRY = "\033[32m██\033[0m"
        EXIT = "\033[1;31m██\033[0m"
        PATH = "\033[1;55m ■\033[0m"

        # path = []
        for y in range(len(self.grid)):
            top = ""
            mid = ""
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]

                if self._is_inside_pattern(x, y):
                    top += SYMB + SYMB
                    mid += SYMB + SYMB
                else:
                    # Top left corner
                    top += WALL
                    # North cell
                    if (cell & self.north_coord):
                        top += WALL
                    elif (x, y -1) in self.path and (x, y) in self.path:
                        top += PATH
                    else:
                        top += FLOOR
                    # top += WALL if (cell & NORTH) else FLOOR

                    # West wall
                    if (cell & self.west_coord):
                        mid += WALL
                    elif (x - 1, y) in self.path and (x, y) in self.path:
                        mid += PATH
                    else:
                        mid += FLOOR
                    # mid += WALL if (cell & WEST) else FLOOR

                    # Floor between walls
                    if y == self.sy and x == self.sx:
                        mid += ENTRY
                    elif y == self.ey and x == self.ex:
                        mid += EXIT
                    elif (x, y) in self.path:
                        mid += PATH
                    else:
                        mid += FLOOR

            # Right most wall/symb
            end_cap = SYMB if self.grid[y][self.width - 1] == 99 else WALL
            print(top + end_cap)
            print(mid + end_cap)

        # Close bottom
        print(WALL * (self.width * 2 + 1))
        ...