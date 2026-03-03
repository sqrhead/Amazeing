

class FileHex:
    def __init__(
            self,
            grid: list[list[int]],
            path: list[tuple[int, int]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            filename: str
            ) -> None:
        self.grid = grid
        self.path = path
        self.entry = entry
        self.exit = exit
        self.filename = filename
        self.hex_table: str = '0123456789ABCDEF'
        self.coords: dict = {
            (0, -1): 'N',
            (0, 1): 'S',
            (-1, 0): 'W',
            (1, 0): 'E'
        }

    def generate(self) -> None:
        with open(self.filename, 'w') as file:
            # Hex map
            for y in range(len(self.grid)):
                if y > 0:
                    file.write('\n')
                for x in range(len(self.grid[0])):
                    hex = self.grid[y][x]
                    if hex == 99:
                        file.write('0')
                    else:
                        file.write(self.hex_table[self.grid[y][x]])
                    ...
            file.write('\n')
            file.write('\n')

            # Coords
            file.write(str(self.entry[0]))
            file.write(', ')
            file.write(str(self.entry[1]))
            file.write('\n')
            file.write(str(self.exit[0]))
            file.write(', ')
            file.write(str(self.exit[1]))

            # Path
            x, y = self.path[0]
            # self.path.remove((x, y))

            file.write('\n')
            for tx, ty in self.path[1:]:
                dx, dy = tx - x, ty - y
                x = tx
                y = ty
                dir = self.coords[(dx, dy)]
                file.write(dir)
            file.write('\n')

