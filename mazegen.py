import random
import math
from time import sleep
from ftsymbol import FTSymbol
from cell import Cell
from collections import deque

'''
- Wall = 0
- Floor = 1
- Symbol = 2
- Start = 3
- End = 4
- Path = 5
'''


#####
#.#.#
#####
#.#.#
#####

# TODO: Switch form Cell class to Array of int based on Hex value

class Maze:
    def __init__(self, width: int, height: int):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        self.width: int  = width
        self.height: int = height
        self.cells: list[Cell] = []

    def get_cell(self, x: int, y: int) -> Cell:
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def is_on_bounds(self, cell: Cell) -> bool:
        if cell.x == self.width - 1  or cell.x == 0:
            return True
        if cell.y == self.height - 1 or cell.y == 0:
            return True
        return False

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        if cell is None:
            return []

        neighbors: list[Cell] = []
        # Here we get the neighbors of 'cell' parameter
        # The cell is added to neighbors only if :
        # - Its not None
        # - Its not visited
        # - Its not on the bounderies of the maze

        for x, y in [(-2,0), (0, -2), (2,0), (0, 2)]:
            neighbor: Cell = self.get_cell(cell.x + x, cell.y + y)

            if neighbor is None:
                continue

            if self.is_on_bounds(neighbor) is True:
                continue

            # type 2 is the 42 symbol
            # if neighbor.type == 2:
            #     continue

            if not neighbor.visited:
                wall = self.get_cell((cell.x + neighbor.x) // 2, (cell.y + neighbor.y) // 2)
                if wall and wall.type == 2:
                    continue
                neighbors.append(neighbor)

        return neighbors

    def generate_grid(self) -> None:
        # TODO: Put here entry/exit cells
        # Create base Grid
        # The grid is created and every '1' cell has 4 walls
        for y in range(self.height):
            for x in range(self.width):
                c: Cell = Cell(x, y)
                self.cells.append(c)
                if y % 2 == 1 and x % 2 == 1:
                    c.type = 1

        # cell_entry = self.get_cell(1, 1)
        # cell_entry.type = 3
        # cell_exit = self.get_cell(self.width -10, self.height -3)
        # cell_exit.type = 4

        # Set cell to 2 for 42 symbol
        # The subject doesnt require to exit if the space is not enough
        # So we return early and not put the 42Symbol on the maze
        if self.width - 2 <= FTSymbol.get_width()  or self.height - 2 <= FTSymbol.get_height():
            print("42SYMBOL: Not enough space in the maze")
            return

        # Coords of the 42 symbol (Top Left)
        start_x = (self.width - FTSymbol.get_width()) // 2
        start_y = (self.height - FTSymbol.get_height()) // 2


        for len_h in range(len(FTSymbol.get_area())):
            for len_w in range(len(FTSymbol.get_area()[0])):
                cell = self.get_cell(start_x + len_w, start_y + len_h)
                match FTSymbol.get_area()[len_h ][len_w]:
                    case '2':
                        cell.type = 2
                        cell.visited = True
                    case '1':
                        cell.type = 1
                        cell.visited = False

    def display_maze(self) -> None:
        print("\033[6;22m******** A MAZE ING *************")
        for y in range(self.height):
            # sleep(0.1)
            print()
            for x in range(self.width):
                cell = self.get_cell(x, y)
                match cell.type:
                    case 0: # Close
                        print("\033[0;33m██", end='')
                    case 1: # Free
                        print("\033[0;30m  ", end='')
                    case 2: # 42 Symbol
                        print("\033[0;46m░░", end='')
                    case 3: # Entry
                        print("\033[1;32m██", end='')
                    case 4: # Exit
                        print("\033[1;31m██", end='')
                    case 5: # Path from Entry to Exit
                        print("\033[1;35m██", end='')
        print()

    def display_on_file(self, file_name: str) -> None:
        with open(file_name, 'w') as file:
            file.write("*** Maze ***\n")
            for y in range(self.height):
                file.write('\n')
                for x in range(self.width):
                    cell = self.get_cell(x, y)
                    match cell.type:
                        case 0:
                            file.write('#')
                        case 1:
                            file.write('.')
                        case 2:
                            file.write('4')

    def create_maze(self) -> None:
        sym_cells = [sym for sym in self.cells if sym.type == 2]
        curr_cell: Cell = self.get_cell(1,1)

        # stack where to put visited cells but unused
        stack: list[Cell] = []
        stack.append(curr_cell)
        stack += sym_cells
        # random.seed(32152136216321532432143213243214321)
        # current cell, the cell where we are going to work on
        # random cell for the moment, later add seed consant behaviour
        rnd_x = random.randrange(1, self.width, 2)
        rnd_y = random.randrange(1, self.height, 2)

        curr_cell: Cell = self.get_cell(1,1)


        if curr_cell is None:
            raise SystemExit("Error: Failed to create Maze\nError: Wrong parameters!!")



        # stack.append(curr_cell)
        # Then we start to loop on the stack
        # And until the stack is empty the loop continues
        # This way the loop moves on every possible way
        # Making this algorithm a good one for 'perfect' maze
        while len(stack) > 0:
            # We get the top on the stack with the -1 way (you get the last element of a list)


            curr_cell = stack[-1]

            # Here we need to check for possible errors
            # It shouldnt happen :>
            if curr_cell is None:
                raise SystemExit("Error: Failed to retrieve Cell from stack")

            # We set the visited to True
            curr_cell.visited = True

            # Then we need to find the next '1' cell we need to go on
            # We do this by finding the neighbors of the curr_cell
            # We use the get_neighbors function since is a bit of logic to put here
            neighbors: list[Cell] = self.get_neighbors(curr_cell)

            # If we dont find neighbors we are at a dead end
            # This means we need to go back and find a cell that has neighbors
            # This is the 'Backtracking' part of the 'Recursive Backtracking Algorithm'
            if len(neighbors) < 1:
                stack.pop()
                continue

            # Now that we have our neighbors, we go and choose one randomly
            # After that we add the others to the stack
            # We also need to remove(set to 1) the wall between the two neighbors
            new_cell = neighbors[random.randint(0, len(neighbors) - 1)]

            # we append it after so its on top, remember this is a stack like push_swap
            stack.append(new_cell)

            # Now we need to set the wall in between to 1, and it will become a tunnel
            # We do this with a simple formula:
            # current cell X + new cell X divided by 2
            # try/except the division zero or it will crash
            wall_x: int = (curr_cell.x + new_cell.x) // 2
            wall_y: int = (curr_cell.y +  new_cell.y) // 2

            wall_cell: Cell = self.get_cell(wall_x, wall_y)

            if wall_cell is None:
                print(f"[ErrorInfo] : Wall.x {curr_cell.x + wall_x}, Wall.y {curr_cell.y + wall_y}")
                raise SystemExit("[Error]: WallCell couldnt be found")

            # the wall is a 42 symbol cell
            # so if use continue to restart the loop
            # if wall_cell.type == 0:
            #     wall_cell.type = 1

            # wall_cell.type = 1
            if wall_cell.type != 2:
                wall_cell.type = 1
            wall_cell.visited = True

            # Here it ends, since we did find the next cell to go on
            # On the next iteration of the loop the new cell will become current
            # and the process will continue until stack is empty
