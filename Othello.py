'''
Name: Matthew Mahan
Studient ID: 103 85 109
Due Date: Nov 13, 2023
Assignment: 3
Section: CSC 475 001
Description: This is an implementation of the board game "Othello" as well as a minimax bot to play it. 
'''
from enum import Enum
import os

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

        outstr += f"Next to move: {(ANSI_FOREGROUND_MAGENTA + "BLACK") if this.blackNextToMove else (ANSI_FOREGROUND_YELLOW + "WHITE")}\n"
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

        # This dictionary holds all of the amounts to add/subtract from an index to move in a particular direction
        directions: dict = {"up": (0, -1), 
                            "up-right": (1, -1), 
                            "right": (1, 0), 
                            "down-right": (1, 1), 
                            "down": (0, 1), 
                            "down-left": (-1, 1), 
                            "left": (-1, 0), 
                            "up-left": (-1, -1)}
        
        # check adjacent tiles for the opposite color on each of the returned next color positions 
        # if there is an opposite tile, follow it out until:
        # 1. an empty tile is found, return the move containing all of the tiles to change to nextColor 
        # 2. the edge of the board is found, return nothing
        # 3. the next color is found, return nothing 
        validMovePositions: dict[position] = {}
        for position in nextColorPositions:
            for direction in directions:

                (x ,y) = position
                vector = directions[direction]
                tilesToFlip = []

                (x, y) = tuple(x+y for x,y in zip((x ,y), vector))
                if (x in range(8) and y in range(8) and this.getTileAt(y, x) != oppositeColor):            # preemptively exit if not the oppenents disc adjacent
                    continue

                while (x in range(8) and y in range(8)):
                    tilesToFlip.append((x, y))
                    if (this.getTileAt(y, x) == Tile.EMPTY):
                        if (x, y) not in validMovePositions:
                            validMovePositions[(x, y)] = []
                        # we want to use extend instead of assignment in case there's multiple paths that can be flipped from a single move 
                        # duplicates will only occur on the move tile, so they're fine and don't affect anything 
                        validMovePositions[(x, y)].extend(tilesToFlip) 
                        break
                    elif (this.getTileAt(y, x) == nextColor):
                        break
                    (x, y) = tuple(x+y for x,y in zip((x ,y), vector))

        return validMovePositions

    # finds all positions of a color on the board 
    def findColorPositions(this, color: Tile) -> list[Position]:

        colorPositions = []

        for i in range(len(this.board)):
            for j in range(len(this.board[0])):
                if this.getTileAt(i, j) == color:
                    colorPositions.append((j, i))

        return colorPositions
    
    def strWithValidMoves(this, validMovePositions: list[Position]) -> str:

        outstr = ANSI_RESTORE_DEFAULT

        outstr += f"Next to move: {(ANSI_FOREGROUND_MAGENTA + "BLACK") if this.blackNextToMove else (ANSI_FOREGROUND_YELLOW + "WHITE")}\n"
        outstr += ANSI_FOREGROUND_WHITE

        # print coordinates for ease of play
        # top coords
        outstr += " "
        for i in range(len(this.board)):
            outstr += (f"{i}" + (" " * (PRINT_WIDTH - 1)))
        outstr += '\n'

        for i in range(len(this.board)):
            rowPrint = ''
            for j in range(len(this.board[0])):
                tilePrint = ANSI_FOREGROUND_GREEN + UNICODE_SHADE_MEDIUM
                if (j, i) in validMovePositions:
                    tilePrint = ANSI_BACKGROUND_WHITE + ANSI_FOREGROUND_YELLOW + UNICODE_SHADE_DARK + ANSI_BACKGROUND_BLACK
                elif this.getTileAt(i, j) == Tile.BLACK:
                    tilePrint = ANSI_FOREGROUND_BLACK + UNICODE_SHADE_FULL
                elif this.getTileAt(i, j) == Tile.WHITE:
                    tilePrint = ANSI_FOREGROUND_WHITE + UNICODE_SHADE_FULL
                rowPrint += tilePrint * PRINT_WIDTH
            outstr += (f"{ANSI_RESTORE_DEFAULT}{i}" + rowPrint + '\n')
            outstr += (" " + rowPrint + '\n') * (PRINT_HEIGHT - 1)

        outstr += ANSI_RESTORE_DEFAULT

        return outstr
    
    # returns true or false based on if the move succeeded or not
    # method assumes that there are > 0 valid moves to play 
    def playMove(this, position: Position, validMoves: dict) -> bool:

        # move fails 
        if position not in validMoves:
            print(f"{position} is not a valid move! Please try again.")
            input("Press enter to continue...")
            return False
        
        # move succeeds
        for coordinate in validMoves[position]:
            this.setTileAt(Tile.BLACK if this.blackNextToMove else Tile.WHITE, coordinate[1], coordinate[0])

        this.blackNextToMove = not this.blackNextToMove
        return True
    
    # check if the game is over
    def isGameOver(this) -> bool:
        nextCanMove = (len(this.findValidMoves()) > 0)
        this.blackNextToMove = not this.blackNextToMove
        oppositeCanMove = (len(this.findValidMoves()) > 0)
        this.blackNextToMove = not this.blackNextToMove

        return not (nextCanMove or oppositeCanMove)
    
    # check the margin of score
    def findMargin(this) -> int:
        total = 0
        for row in this.board:
            for tile in row:
                total += tile.value # in the enum, black is -1, white is 1, and empty is 0, so they can be easily summed 

        return total
    
class Menu:

    game = None
    DEBUG = False

    def __init__(this):
        this.DEBUG = False
        this.game = Oth()

    def printList(this, items: dict) -> None: 
        for i in range(len(items)):
            print(f"[{i}] {items[i][0]}")

    def clearConsole(this) -> None:
        os.system('cls')

    def getInput(this):
        return input(">>> ").strip()

    # entry point for the program
    def startScreen(this) -> None:

        # table of options and their functions 
        options: dict = {0: ("Exit", lambda: exit()), 
                         1: ("Begin two player game", lambda: this.twoPlayer()), 
                         2: ("Begin bot game", lambda: this.botPlayer())}

        # menu stuff
        this.clearConsole()
        print(f"{ANSI_BACKGROUND_GREEN}{ANSI_FOREGROUND_WHITE}Welcome to Othello!{ANSI_RESTORE_DEFAULT}")
        this.printList(options)
        userIn = int(this.getInput())

        # run the selection 
        # unsafe, doesn't check the input, but whateverrrr mannnnn
        options[userIn][1]()

    # plays a move for a human
    def playCoordinate(this) -> None:

        # printing 
        this.clearConsole()
        validMoves = this.game.findValidMoves()
        print(this.game.strWithValidMoves(validMoves))

        if len(validMoves) == 0:
            print(f"{ANSI_FOREGROUND_MAGENTA + "BLACK" if this.game.blackNextToMove else ANSI_FOREGROUND_YELLOW + "WHITE"}{ANSI_RESTORE_DEFAULT} has no valid moves and must pass.")
            input("Press enter to continue...")
            this.game.blackNextToMove = not this.game.blackNextToMove
        else:
            print("Type the coordinate to play as a tuple like (x, y). Valid moves are highlighted yellow.")

            userIn = this.getInput()
            userIn = userIn.strip('(')
            userIn = userIn.strip(')')
            coordinate = tuple(map(int, userIn.split(', ')))

            this.game.playMove(coordinate, this.game.findValidMoves())

    def enableDebug(this) -> None:
        pass

    # run basic game with humans
    def twoPlayer(this) -> None:

        actions = {0: ("Exit", lambda: exit()),
                   1: ("Play move", lambda: this.playCoordinate()),
                   2: ("Enable debug", lambda: this.enableDebug())}

        # main game loop
        while not this.game.isGameOver():
            this.clearConsole()
            print(this.game)
            this.printList(actions)
            userIn = int(this.getInput())
            actions[userIn][1]()

        # end game state
        margin = this.game.findMargin()
        if margin > 0:
            this.clearConsole()
            print(this.game)
            print(f"{ANSI_FOREGROUND_YELLOW}WHITE{ANSI_FOREGROUND_WHITE} wins with a margin of {abs(margin)}!")
        elif margin < 0:
            this.clearConsole()
            print(this.game)
            print(f"{ANSI_FOREGROUND_MAGENTA}BLACK{ANSI_FOREGROUND_WHITE} wins with a margin of {abs(margin)}!")
        else:
            this.clearConsole()
            print(this.game)
            print(f"It's a draw!")

    def botPlayer(this) -> None:
        print("bot player")

if __name__ == "__main__":
    menu = Menu()
    menu.startScreen()