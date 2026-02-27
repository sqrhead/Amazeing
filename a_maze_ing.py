import random
import sys

from pathfinder import Pathfinder
from mazegen import Maze
from parser import Parser

# TODO: Divide code to make it cleaner
# TODO: BFS is a little broky
# TODO: Number 2 breaks perfect sometimes

if __name__ == "__main__":
    # Create Maze class instance
    parser: Parser = Parser()
    config_data = parser.config()
    # maze: Maze = Maze(config_data['WIDTH'],config_data['HEIGHT'])
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    maze: Maze = Maze(n1, n2)

    # Generate Maze
    maze.generate_grid()
    maze.create_maze()

    # Pathfinder
    # pathfinder: Pathfinder = Pathfinder(maze.cells)
    # free_cells = [cell for cell in maze.cells if cell.type == 1]
    # path = pathfinder.get_path(maze.get_cell(1,1), free_cells[-1])

    # if len(path) > 0:
    #     for cell in path:
    #         new_c = maze.get_cell(cell.x, cell.y)
    #         new_c.type = 5

    #     path[0].type = 3
    #     path[-1].type = 4

    # Display
    maze.display_maze()
    maze.display_on_file('mdisplay.txt')


    print("\033[1;37m0)Regen 1)Path 3)Color 4)Quit")
    print("\x1b[0m") # Reset ansi code color


    # print("┏━━━━━━━━━━┓")
    # print("┃          ┃")
    # print("┣   DAWG   ┫")
    # print("┃          ┃")
    # print("┗━━━━━━━━━━┛")


# ASCII
# Light
# ▓ ░
# Heavy
# █  heavy block
# Double block
# ██
# Cooler
# ┃ ━ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋