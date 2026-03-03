import random
import sys
import os

from mazegen import MazeGenerator
from mazegen import Pathfinder
from mazegen import FileHex
from mazegen import Parser
from mazegen import Displayer

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 a_maze_ing.py <file_name(.txt)>")

    config_file = sys.argv[1]
    parser: Parser = Parser()
    config_data = parser.config(config_file)

    maze_gen: MazeGenerator = MazeGenerator(
        config_data['WIDTH'],
        config_data['HEIGHT'],
        config_data['ENTRY'],
        config_data['EXIT'],
        config_data['SEED']
        )
    grid = maze_gen.generate(config_data['PERFECT'])

    pathfinder: Pathfinder = Pathfinder(maze_gen.grid)
    path: list[tuple[int, int]] = pathfinder.get_path(
        config_data['ENTRY'],
        config_data['EXIT']
        )

    displayer: Displayer = Displayer(
        maze_gen.grid,
        path,
        config_data['ENTRY'],
        config_data['EXIT'],
        maze_gen.pattern_cells
        )
    filehex: FileHex = FileHex(
        grid,
        path,
        config_data['ENTRY'],
        config_data['EXIT'],
        config_data['OUTPUT_FILE']
        )
    filehex.generate()

    choice = '1'
    path_flag = False
    while choice != '4':

        if os.name == 'nt':  # Windows
            os.system('cls')
        else:
            os.system('clear')

        displayer.display(path_flag)
        print("==== A MAZE ING =====")
        print("1) Re-generate maze")
        print("2) Show/Hide path")
        print("3) Rotate maze colors")
        # ctrl-c crash
        print("4 / CTRL-C) Quit")
        try:
            choice = input("Choice: ").strip()
        except KeyboardInterrupt:
            print()
            raise SystemExit()

        if choice == '1':
            maze_gen: MazeGenerator = MazeGenerator(
                config_data['WIDTH'],
                config_data['HEIGHT'],
                config_data['ENTRY'],
                config_data['EXIT'],
                random.randint(1, 2**32)
                )
            grid = maze_gen.generate(config_data['PERFECT'])

            pathfinder.grid = grid

            path = pathfinder.get_path(
                config_data['ENTRY'],
                config_data['EXIT']
                )

            displayer.grid = grid

            displayer.pattern_cells = maze_gen.pattern_cells
            displayer.path = path

            filehex.grid = grid
            filehex.path = path
            filehex.generate()

        elif choice == '2':
            path_flag = not path_flag

        elif choice == '3':
            displayer.set_next_color()

        else:
            continue
