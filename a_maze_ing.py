from pathfinder import Pathfinder
from mazegen import Maze

# TODO: Divide code to make it cleaner
# TODO: BFS is a little broky
# TODO: Number 2 breaks perfect sometimes

if __name__ == "__main__":
    # Create Maze class instance
    maze: Maze = Maze(50,30)

    # Generate Maze
    maze.generate_grid()
    maze.create_maze()

    # Pathfinder
    pathfinder: Pathfinder = Pathfinder(maze.cells)
    path = pathfinder.get_path(maze.get_cell(1,1), maze.get_cell(5,1))

    for cell in path:
        new_c = maze.get_cell(cell.x, cell.y)
        new_c.type = 5

    path[0].type = 3
    path[-1].type = 4

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