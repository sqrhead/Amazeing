

class FileHex:
    def __init__(self, grid: list[list[int]], path: list[tuple[int, int]], filename: str) -> None:
        self.grid = grid
        self.path = path
        self.filename = filename
        self.hex_table: str = '0123456789ABCDEF'

    def generate(self) -> None:
        with open(self.filename, 'w') as file:
            for y in range(len(self.grid)):
                file.write('\n')
                for x in range(len(self.grid[0])):
                    hex = self.grid[y][x]
                    if hex == 99:
                        file.write('F')
                    else:
                        file.write(self.hex_table[self.grid[y][x] - 1])
                    ...
            file.write('\n')