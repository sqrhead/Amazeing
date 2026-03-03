

class FileHex:
    """Writes the maze grid and path to a hexadecimal output file.

    Each cell is encoded as a single hex digit where each bit represents
    a wall direction (N=1, E=2, S=4, W=8). The output file also contains
    the entry/exit coordinates and the shortest path as cardinal directions.

    Attributes:
        grid: 2D list of integers encoding wall states per cell.
        path: List of (x, y) coordinates representing the shortest path.
        entry: (x, y) coordinates of the maze entry point.
        exit: (x, y) coordinates of the maze exit point.
        filename: Name of the output file to write to.
    """
    def __init__(
            self,
            grid: list[list[int]],
            path: list[tuple[int, int]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            filename: str
            ) -> None:
        """Initialize FileHex with maze data and output filename.

            Args:
                grid: 2D list of integers encoding wall states per cell.
                path: List of (x, y) coordinates of the shortest path.
                entry: (x, y) coordinates of the maze entry point.
                exit: (x, y) coordinates of the maze exit point.
                filename: Path to the output file.
        """
        self.grid = grid
        self.path = path
        self.entry = entry
        self.exit = exit
        self.filename = filename
        self.hex_table: str = '0123456789ABCDEF'
        self.coords: dict[tuple[int, int], str] = {
            (0, -1): 'N',
            (0, 1): 'S',
            (-1, 0): 'W',
            (1, 0): 'E'
        }

    def generate(self) -> None:
        """Write the maze grid, coordinates and path to the output file.

        The output format is:
            - One hex digit per cell, one row per line.
            - An empty line separator.
            - Entry coordinates as 'x,y'.
            - Exit coordinates as 'x,y'.
            - Shortest path as a sequence of N/S/E/W characters.
            - 'no path' if no path exists between entry and exit.
        """
        with open(self.filename, 'w') as file:
            # Hex map
            for y in range(len(self.grid)):
                if y > 0:
                    file.write('\n')
                for x in range(len(self.grid[0])):
                    file.write(self.hex_table[self.grid[y][x]])
                    ...
            file.write('\n')
            file.write('\n')

            # Coords
            file.write(str(self.entry[0]))
            file.write(',')
            file.write(str(self.entry[1]))
            file.write('\n')
            file.write(str(self.exit[0]))
            file.write(',')
            file.write(str(self.exit[1]))

            # Path
            try:
                x, y = self.path[0]
            except IndexError:
                file.write('\n')
                file.write("no path")
                file.write('\n')
                return
            file.write('\n')
            for tx, ty in self.path[1:]:
                dx, dy = tx - x, ty - y
                x = tx
                y = ty
                dir = self.coords[(dx, dy)]
                file.write(dir)
            file.write('\n')
