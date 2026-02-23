import random
from enum import Enum
from typing import Callable

# Algo for the maze: Recursive Backtracking

class TileType:

    # WALL = '█'

    # FLOOR = ' '

    WALL = '#'
    FLOOR = 'o'

class Tile:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

        self.type: TileType = TileType.WALL


class Maze:
    def __init__(self, width: int, height: int):
        self.width:int  = width
        self.height: int = height
        self.tiles: list[list[Tile]] = []


    def get_tile(self, m_map: list[list[Tile]], x: int, y: int) -> Tile:
        for i in m_map:
            for j in i:
                if j.x == x and j.y == y:
                    return j
        return None
        # raise Exception(f"Error: Tile not found\nTile Info: x:{x} y:{y}")


    def generate(self) -> None:
        m_map = []
        for y in range(self.height):
            m_map.append([])
            for x in range(self.width):
                m_map[y].append(Tile(x, y))

        try:
            # rnd_t = m_map[0][0]
            rnd_t = self.get_tile(m_map, random.randint(0, len(m_map) -1), random.randint(0, len(m_map[0]) -1))
            rnd_t.type = TileType.FLOOR
            stack: list = [ rnd_t ]
            walls: list = []

            while rnd_t is not None:
                for i in [-2, 2]:
                    for j in [-2, 2]:
                        x_tile = self.get_tile(m_map, rnd_t.x + i, rnd_t.y)
                        if x_tile is not None:
                            if x_tile.type is not TileType.FLOOR:
                                walls.append(x_tile)

                        y_tile = self.get_tile(m_map, rnd_t.x, rnd_t.y + j)
                        if y_tile is not None:
                            if y_tile.type is not TileType.FLOOR:
                                walls.append(y_tile)

                if len(walls) > 0:
                    rnd_t = walls[random.randint(0, len(walls))]
                    rnd_t.type = TileType.FLOOR

            # print(f"rnd_t x: {rnd_t.x}, y: {rnd_t.y}")
        except Exception as e:
            print(f"{e}")

        self.tile = m_map


if __name__ == "__main__":
    maze: Maze = Maze(51, 25)
    maze.generate()

    with open('maze_display.txt', 'w') as file:
        file.write("*** Maze ***\n")
        for y in maze.tile:
            file.write("\n")
            for x in y:
                file.write(x.type)