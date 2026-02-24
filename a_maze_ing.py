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

    def generate(self) -> None:
        m_map = []
        for y in range(self.height):
            m_map.append([])
            for x in range(self.width):
                m_map[y].append(Tile(x, y))
                # if x % 2 == 0 or y % 2 == 0:
                #     m_map[y][x].type = TileType.WALL
        
        self.tile = m_map

        # for y in range(self.height):
        #     for x in range(self.width):
        #         if m_map[y][x].type is TileType.FLOOR:
        #             self.free_tiles.append(m_map[y][x])
        
        curr_t = m_map[self.height // 2][self.width // 2]
        curr_t.type = TileType.FLOOR
        walls = []

        while curr_t is not None:
            for y in [-1, 1]:
                for x in [-1, 1]:
                    x_tile = m_map[curr_t.y][curr_t.x + x]
                    y_tile = m_map[curr_t.y + y][curr_t.x]
                    if x_tile.type is not TileType.FLOOR:
                        walls.append(m_map[curr_t.y][curr_t.x + x])
                    if y_tile.type is not TileType.FLOOR:
                        walls.append(m_map[curr_t.y + y][curr_t.x])
            print(f"N of walls : {len(walls)}")
            try:            
                curr_t = walls[random.randint(0, len(walls))]
                curr_t.type = TileType.FLOOR
            except IndexError:
                curr_t = None
            walls.clear()


if __name__ == "__main__":
    maze: Maze = Maze(51, 25)
    maze.generate()

    with open('maze_display.txt', 'w') as file:
        file.write("*** Maze ***\n")
        for tile_l in maze.tile:
            file.write("\n")
            for tile in tile_l:
                file.write(tile.type)
        