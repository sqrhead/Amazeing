import random
from enum import Enum

# Algo for the maze: Recursive Backtracking

class TileType:
    WALL=0
    TILE=0

class Tile:
    def __init__(self, x: int, y: int):
        self.x: int  = x
        self.y: int  = y
        self.type: TileType  = TileType.WALL

class Maze:
    def __init__(self,width: int, height: int):
        self.width:int  = width
        self.height: int = height

    def generate(self) -> list[Tile]:
        ...

if __name__ == "__main__":
    ...