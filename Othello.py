'''
Name: Matthew Mahan
Studient ID: 103 85 109
Due Date: Nov 13, 2023
Assignment: 3
Section: CSC 475 001
Description: This is an implementation of the board game "Othello" as well as a minimax bot to play it. 
'''
from enum import Enum

# custom type hints 
type Matrix = list[list[Tile]]
type Position = tuple[int, int]
type Move = tuple[Tile, list[Position]]

# formatting constants
ANSI_FOREGROUND_BLACK = '\x1b[30m'
ANSI_FOREGROUND_RED = '\x1b[31m'
ANSI_FOREGROUND_GREEN = '\x1b[32m'
ANSI_FOREGROUND_YELLOW = '\x1b[33m'
ANSI_FOREGROUND_BLUE = '\x1b[34m'
ANSI_FOREGROUND_MAGENTA = '\x1b[35m'
ANSI_FOREGROUND_CYAN = '\x1b[36m'
ANSI_FOREGROUND_WHITE = '\x1b[37m'

ANSI_BACKGROUND_BLACK = '\x1b[40m'
ANSI_BACKGROUND_RED = '\x1b[41m'
ANSI_BACKGROUND_GREEN = '\x1b[42m'
ANSI_BACKGROUND_YELLOW = '\x1b[43m'
ANSI_BACKGROUND_BLUE = '\x1b[44m'
ANSI_BACKGROUND_MAGENTA = '\x1b[45m'
ANSI_BACKGROUND_CYAN = '\x1b[46m'
ANSI_BACKGROUND_WHITE = '\x1b[47m'

ANSI_RESTORE_DEFAULT = ANSI_FOREGROUND_WHITE + ANSI_BACKGROUND_BLACK

UNICODE_SHADE_FULL = '█'
UNICODE_SHADE_DARK = '▓'
UNICODE_SHADE_MEDIUM = '▒'
UNICODE_SHADE_LIGHT = '░'
UNICODE_SHADE_EMPTY = ' '

PRINT_WIDTH = 4
PRINT_HEIGHT = 2

# create an enum to define what can go in a board tile 
class Tile(Enum):
    EMPTY = 0
    BLACK = -1 # the user will always start and black always starts, so black has a negative heuristic association
    WHITE = 1

# game class (rules and board)
class Oth: 

    # members 
    board: Matrix = None
    blackNextToMove: bool = None

    # construct a new game
    def __init__(this):
        this.board = Oth.createStartBoard()
        this.blackNextToMove = True

    # return the starting board 
    def createStartBoard() -> Matrix:
        E = Tile.EMPTY
        B = Tile.BLACK
        W = Tile.WHITE
        return [[E, E, E, E, E, E, E, E],
                [E, E, E, E, E, E, E, E],
                [E, E, E, E, E, E, E, E],
                [E, E, E, W, B, E, E, E],
                [E, E, E, B, W, E, E, E],
                [E, E, E, E, E, E, E, E],
                [E, E, E, E, E, E, E, E],
                [E, E, E, E, E, E, E, E]]
    
    # accessors and mutators 
    def getTileAt(this, i: int, j: int) -> Tile:
        return this.board[i][j]
    
    def setTileAt(this, tile: Tile, i: int, j: int) -> None:

        if i not in range(0, 8):
            return
        if j not in range(0, 8):
            return
        
        this.board[i][j] = tile

    # formatted printing
    def __str__(this) -> str:
        
        outstr = ANSI_RESTORE_DEFAULT

        outstr += f"Next to move: {(ANSI_FOREGROUND_MAGENTA + "BLACK") if this.blackNextToMove else (ANSI_FOREGROUND_WHITE + "WHITE")}\n"
        outstr += ANSI_FOREGROUND_WHITE

        for row in this.board:
            rowPrint = ''
            for tile in row:
                tilePrint = ANSI_FOREGROUND_GREEN + UNICODE_SHADE_MEDIUM
                if tile == Tile.BLACK:
                    tilePrint = ANSI_FOREGROUND_BLACK + UNICODE_SHADE_FULL
                elif tile == Tile.WHITE:
                    tilePrint = ANSI_FOREGROUND_WHITE + UNICODE_SHADE_FULL
                rowPrint += tilePrint * PRINT_WIDTH
            outstr += (rowPrint + '\n') * PRINT_HEIGHT

        outstr += ANSI_RESTORE_DEFAULT

        return outstr

    # searches the board and returns a list of tuples which are valid coordinates for next player to place a tile
    def findValidMoves(this) -> list[Position]:

        nextColor = Tile.WHITE
        oppositeColor = Tile.BLACK
        if this.blackNextToMove:
            nextColor = Tile.BLACK
            oppositeColor = Tile.WHITE

        # find next player's color tiles in the board
        nextColorPositions = this.findColorPositions(nextColor)

        # check adjacent tiles for the opposite color on each of the returned next color positions 
        # if there is an opposite tile, follow it out until:
        # 1. an empty tile is found, return the move containing all of the tiles to change to nextColor 
        # 2. the edge of the board is found, return None 
        # 3. the next color is found, return None 
        for position in nextColorPositions:
            pass


    # finds all positions of a color on the board 
    def findColorPositions(this, color: Tile) -> list[Position]:

        colorPositions = []

        for i in range(this.board):
            for j in range(i):
                if this.getTileAt(i, j) == color:
                    colorPositions.append((i, j))

        return colorPositions


if __name__ == "__main__":
    oth = Oth()
    print(oth)