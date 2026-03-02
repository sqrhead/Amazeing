from mazegen import MazeGenerator
from filehex import FileHex
from pathfinder import Pathfinder
from parser import Parser
# [TODO] Create display class ?????

if __name__ == "__main__":
    parser: Parser = Parser()
    config_data = parser.config()

    mg: MazeGenerator = MazeGenerator()
    pathfinder: Pathfinder = Pathfinder()
    flhex: FileHex = FileHex()

    ...


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
# Bot
# ▄
# Top
# ▀

# ■