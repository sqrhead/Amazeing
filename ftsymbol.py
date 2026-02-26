'''
........
#....###
#......#
###..###
..#..#..
..#..###
........

'''

class FTSymbol:

    @staticmethod
    def get_area() -> list[list[str]]:
        area: list[list[str]] = [
            ["#",".",".",".","#","#","#"],
            ["#",".","#",".",".",".","#"],
            ["#","#","#",".","#","#","#"],
            [".",".","#",".","#",".","."],
            [".",".","#",".","#","#","#"],
        ]
        return area

    @staticmethod
    def get_width() -> int:
        return 7

    @staticmethod
    def get_height() -> int:
        return 5

    @staticmethod
    def get_closed_cell_type() -> str:
        return '#'

    @staticmethod
    def get_open_cell_type() -> str:
        return '.'
    ...
