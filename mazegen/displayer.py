
class Displayer:
    """Renders the maze in the terminal using ANSI color codes.

    Displays the maze grid as a 2D ASCII art with colored walls,
    entry/exit markers, the 42 pattern, and an optional shortest path.
    Supports wall color rotation through user interaction.

    Attributes:
        grid: 2D list encoding wall states per cell as integers.
        path: List of (x, y) coordinates of the shortest path.
        sx: Column index of the entry point.
        sy: Row index of the entry point.
        ex: Column index of the exit point.
        ey: Row index of the exit point.
        pattern_cells: List of (x, y) coordinates of the 42 pattern.
        width: Number of cells horizontally.
        height: Number of cells vertically.
    """
    def __init__(
            self,
            grid: list[list[int]],
            path: list[tuple[int, int]],
            start: tuple[int, int],
            end: tuple[int, int],
            pattern_cells: list[tuple[int, int]]
            ) -> None:
        """Initialize the displayer with maze data.

        Args:
            grid: 2D list of integers encoding wall states per cell.
            path: List of (x, y) coordinates of the shortest path.
            start: (x, y) coordinates of the maze entry point.
            end: (x, y) coordinates of the maze exit point.
            pattern_cells: List of (x, y) coords of the 42 pattern.

        Raises:
            SystemExit: If entry or exit overlap with a pattern cell.
        """
        self.grid = grid
        self.path = path
        self.sx, self.sy = start
        self.ex, self.ey = end
        self.pattern_cells = pattern_cells
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self._wall_colors = [
            "\033[1;33m",
            "\033[1;53m",
            "\033[0;35m",
            "\033[0;36m",
            "\033[1;31m",
        ]
        if start in pattern_cells:
            raise SystemExit("[Error] Config file, ENTRY value on SYMBOL")

        if end in pattern_cells:
            raise SystemExit("[Error] Config file, EXIT value on SYMBOL")

    def set_next_color(self) -> None:
        """Rotate the wall color to the next one in the color list.

        Moves the current color to the end of the list, making the
        next color active on the following display call.
        """

        color = self._wall_colors[0]
        self._wall_colors.remove(color)
        self._wall_colors.append(color)

    def display(self, show_path: bool = False) -> None:
        """Render the maze in the terminal using ANSI color codes.

        Draws each cell row by row with top and middle lines.
        Walls, floors, entry, exit, pattern cells and the optional
        path are each rendered with distinct colors.

        Args:
            show_path: If True, renders the shortest path overlay.
                       Defaults to False.
        """
        WALL = self._wall_colors[0] + "██\033[0m"
        FLOOR = "  "
        SYMB = "\033[0;36m██\033[0m"
        ENTRY = "\033[32m██\033[0m"
        EXIT = "\033[1;31m██\033[0m"
        PATH = "\033[1;55m ■\033[0m"
        NORTH = 1
        WEST = 8

        for y in range(self.height):
            top = ""
            mid = ""
            for x in range(self.width):
                cell = self.grid[y][x]

                if (x, y) in self.pattern_cells:
                    top += SYMB + SYMB
                    mid += SYMB + SYMB
                else:
                    # Top left corner
                    top += WALL
                    # North cell
                    if (cell & NORTH):
                        top += WALL
                    elif (x, y - 1) in self.path and \
                            (x, y) in self.path and show_path:
                        top += PATH
                    else:
                        top += FLOOR
                    # top += WALL if (cell & NORTH) else FLOOR

                    # West wall
                    if (cell & WEST):
                        mid += WALL
                    elif (x - 1, y) in self.path and \
                            (x, y) in self.path and show_path:
                        mid += PATH
                    else:
                        mid += FLOOR
                    # mid += WALL if (cell & WEST) else FLOOR

                    # Floor between walls
                    if y == self.sy and x == self.sx:
                        mid += ENTRY
                    elif y == self.ey and x == self.ex:
                        mid += EXIT
                    elif (x, y) in self.path and show_path:
                        mid += PATH
                    else:
                        mid += FLOOR

            # Right most wall/symb
            end_cap = ""
            if (self.width - 1, y) in self.pattern_cells:
                end_cap += SYMB
            else:
                end_cap += WALL

            # end_cap = SYMB if self.grid[y][self.width-1] == 99 else WALL
            print(top + end_cap)
            print(mid + end_cap)

        # Close bottom
        print(WALL * (self.width * 2 + 1))
