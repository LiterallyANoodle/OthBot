'''
Name: Matthew Mahan
Studient ID: 103 85 109
Due Date: Nov 13, 2023
Assignment: 3
Section: CSC 475 001
Description: This is an implementation of the board game "Othello" as well as a minimax bot to play it. 
'''
from enum import Enum
from random import randrange
import os
import warnings

# ignore syntax warnings 
warnings.filterwarnings(action='ignore', category=SyntaxWarning)

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

PRINT_WIDTH = 8
PRINT_HEIGHT = 4

SEARCH_DEPTH = 6

TITLE_ASCII_ART_1 = \
"""
+===========================================================================+
| ________  _________  ___  ___  _______   ___       ___       ________     |
||\   __  \|\___   ___\\\  \|\  \|\  ___ \ |\  \     |\  \     |\   __  \    |
|\ \  \|\  \|___ \  \_\ \  \\\\\  \ \   __/|\ \  \    \ \  \    \ \  \|\  \   |
| \ \  \\\\\  \   \ \  \ \ \   __  \ \  \_|/_\ \  \    \ \  \    \ \  \\\\\  \  |
|  \ \  \\\\\  \   \ \  \ \ \  \ \  \ \  \_|\ \ \  \____\ \  \____\ \  \\\\\  \ |
|   \ \_______\   \ \__\ \ \__\ \__\ \_______\ \_______\ \_______\ \_______\|
|    \|_______|    \|__|  \|__|\|__|\|_______|\|_______|\|_______|\|_______||
+===========================================================================+
"""
TITLE_ASCII_ART_2 = \
"""
+==============================================================================================+
|         _          _            _       _    _            _             _             _      |
|        /\ \       /\ \         / /\    / /\ /\ \         _\ \          _\ \          /\ \    |
|       /  \ \      \_\ \       / / /   / / //  \ \       /\__ \        /\__ \        /  \ \   |
|      / /\ \ \     /\__ \     / /_/   / / // /\ \ \     / /_ \_\      / /_ \_\      / /\ \ \  |
|     / / /\ \ \   / /_ \ \   / /\ \__/ / // / /\ \_\   / / /\/_/     / / /\/_/     / / /\ \ \ |
|    / / /  \ \_\ / / /\ \ \ / /\ \___\/ // /_/_ \/_/  / / /         / / /         / / /  \ \_\|
|   / / /   / / // / /  \/_// / /\/___/ // /____/\    / / /         / / /         / / /   / / /|
|  / / /   / / // / /      / / /   / / // /\____\/   / / / ____    / / / ____    / / /   / / / |
| / / /___/ / // / /      / / /   / / // / /______  / /_/_/ ___/\ / /_/_/ ___/\ / / /___/ / /  |
|/ / /____\/ //_/ /      / / /   / / // / /_______\/_______/\__\//_______/\__\// / /____\/ /   |
|\/_________/ \_\/       \/_/    \/_/ \/__________/\_______\/    \_______\/    \/_________/    |
+==============================================================================================+
"""
TITLE_ASCII_ART_3 = \
"""
+========================================================================+
|    ,----..                                                             |
|   /   /   \      ___      ,---,                ,--,    ,--,            |
|  /   .     :   ,--.'|_  ,--.' |              ,--.'|  ,--.'|            |
| .   /   ;.  \  |  | :,' |  |  :              |  | :  |  | :     ,---.  |
|.   ;   /  ` ;  :  : ' : :  :  :              :  : '  :  : '    '   ,'\ |
|;   |  ; \ ; |.;__,'  /  :  |  |,--.   ,---.  |  ' |  |  ' |   /   /   ||
||   :  | ; | '|  |   |   |  :  '   |  /     \ '  | |  '  | |  .   ; ,. :|
|.   |  ' ' ' ::__,'| :   |  |   /' : /    /  ||  | :  |  | :  '   | |: :|
|'   ;  \; /  |  '  : |__ '  :  | | |.    ' / |'  : |__'  : |__'   | .; :|
| \   \  ',  /   |  | '.'||  |  ' | :'   ;   /||  | '.'|  | '.'|   :    ||
|  ;   :    /    ;  :    ;|  :  :_:,''   |  / |;  :    ;  :    ;\   \  / |
|   \   \ .'     |  ,   / |  | ,'    |   :    ||  ,   /|  ,   /  `----'  |
|    `---`        ---`-'  `--''       \   \  /  ---`-'  ---`-'           |
|                                      `----'                            |
+========================================================================+
"""
TITLE_ASCII_ART_4 = \
"""
+=================================================================================+
| ▄██████▄      ███        ▄█    █▄       ▄████████  ▄█        ▄█        ▄██████▄ |
|███    ███ ▀█████████▄   ███    ███     ███    ███ ███       ███       ███    ███|
|███    ███    ▀███▀▀██   ███    ███     ███    █▀  ███       ███       ███    ███|
|███    ███     ███   ▀  ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███       ███    ███|
|███    ███     ███     ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███       ███    ███|
|███    ███     ███       ███    ███     ███    █▄  ███       ███       ███    ███|
|███    ███     ███       ███    ███     ███    ███ ███▌    ▄ ███▌    ▄ ███    ███|
| ▀██████▀     ▄████▀     ███    █▀      ██████████ █████▄▄██ █████▄▄██  ▀██████▀ |
|                                                   ▀         ▀                   |
+=================================================================================+
"""
TITLE_ASCII_ART_5 = \
"""
+===================================================================+
| ▄▀▀▀▀▄   ▄▀▀▀█▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄    ▄▀▀▀▀▄    ▄▀▀▀▀▄ |
|█      █ █    █  ▐ █  █   ▄▀ ▐  ▄▀   ▐ █    █    █    █    █      █|
|█      █ ▐   █     ▐  █▄▄▄█    █▄▄▄▄▄  ▐    █    ▐    █    █      █|
|▀▄    ▄▀    █         █   █    █    ▌      █         █     ▀▄    ▄▀|
|  ▀▀▀▀    ▄▀         ▄▀  ▄▀   ▄▀▄▄▄▄     ▄▀▄▄▄▄▄▄▀ ▄▀▄▄▄▄▄▄▀ ▀▀▀▀  |
|         █          █   █     █    ▐     █         █               |
|         ▐          ▐   ▐     ▐          ▐         ▐               |
+===================================================================+
"""




# create an enum to define what can go in a board tile 
class Tile(Enum):
    EMPTY = 0
    BLACK = -1 # the user will usually start and black always starts, so black has a negative heuristic association typically
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
        # return [[W, E, B, E, B, E, E, E],
        #         [E, W, W, W, W, W, W, E],
        #         [B, E, W, E, B, E, E, E],
        #         [E, W, E, W, W, W, W, E],
        #         [W, E, W, B, W, B, E, E],
        #         [E, W, E, W, E, W, B, B],
        #         [E, E, W, E, E, B, B, B],
        #         [E, E, E, E, E, B, B, B]]
    
    # accessors and mutators 
    def getTileAt(this, i: int, j: int) -> Tile:
        return this.board[i][j]
    
    def setTileAt(this, tile: Tile, i: int, j: int) -> None:

        if i not in range(0, 8):
            return
        if j not in range(0, 8):
            return
        
        this.board[i][j] = tile

    def getBoardClone(this, inBoard):
        outBoard = []

        for i in range(len(inBoard)):
            outBoard.append([])
            for j in range(len(inBoard[0])):
                outBoard[i].append(inBoard[i][j])

        return outBoard

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

    # string with no special characters or ANSI codes for outputting to file 
    def strForOutput(this, inBoard=None, inBlackNextToMove=None) -> str:

        printBoard = this.board
        printBlackNextMove = this.blackNextToMove

        # allows for printing of either this game's board or any arbitrary board 
        if inBoard != None and inBlackNextToMove != None:
            printBoard = inBoard
            printBlackNextMove = inBlackNextToMove

        outstr = f"Next to move: {"BLACK" if printBlackNextMove else "WHITE"}\n"

        for i in range(len(printBoard)):
            rowPrint = "["
            for j in range(len(printBoard[0])):
                if printBoard[i][j] == Tile.EMPTY:
                    rowPrint += ". "
                elif printBoard[i][j] == Tile.BLACK:
                    rowPrint += "B "
                elif printBoard[i][j] == Tile.WHITE:
                    rowPrint += "W "
            rowPrint += f"]\n"
            outstr += rowPrint

        outstr += f"Valid moves: {list(this.findValidMoves(inBoard=printBoard, inBlackNextMove=printBlackNextMove).keys())}"

        return outstr

    # searches the board and returns a list of tuples which are valid coordinates for next player to place a tile
    def findValidMoves(this, inBoard=None, inBlackNextMove=None) -> list[Position]:

        checkBoard = this.board
        checkBlackNextMove = this.blackNextToMove

        # allow an arbitrary board to be passed in
        if inBoard != None and inBlackNextMove != None:
            checkBoard = inBoard
            checkBlackNextMove = inBlackNextMove

        nextColor = Tile.WHITE
        oppositeColor = Tile.BLACK
        if checkBlackNextMove:
            nextColor = Tile.BLACK
            oppositeColor = Tile.WHITE

        # find next player's color tiles in the board
        nextColorPositions = this.findColorPositions(nextColor, checkBoard)

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
                if (x in range(8) and y in range(8) and checkBoard[y][x] != oppositeColor):            # preemptively exit if not the oppenents disc adjacent
                    continue

                while (x in range(8) and y in range(8)):
                    tilesToFlip.append((x, y))
                    if (checkBoard[y][x] == Tile.EMPTY):
                        if (x, y) not in validMovePositions:
                            validMovePositions[(x, y)] = []
                        # we want to use extend instead of assignment in case there's multiple paths that can be flipped from a single move 
                        # duplicates will only occur on the move tile, so they're fine and don't affect anything 
                        validMovePositions[(x, y)].extend(tilesToFlip) 
                        break
                    elif (checkBoard[y][x] == nextColor):
                        break
                    (x, y) = tuple(x+y for x,y in zip((x ,y), vector))

        return validMovePositions

    # finds all positions of a color on the board 
    def findColorPositions(this, color: Tile, inBoard: Matrix) -> list[Position]:

        colorPositions = []

        for i in range(len(inBoard)):
            for j in range(len(inBoard[0])):
                if inBoard[i][j] == color:
                    colorPositions.append((j, i))

        return colorPositions
    
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

    # returns the resulting board after a move 
    def simulateMove(this, playBoard: Matrix, blackNextToMove: bool, position: Position, validMoves: dict) -> Matrix:

        # extra board to hold the resultant state and return
        extraBoard = this.getBoardClone(playBoard)
        
        # set the appropriate tiles associated with the move
        # assumes a valid move was passed in
        for coordinate in validMoves[position]:
            extraBoard[coordinate[1]][coordinate[0]] = (Tile.BLACK if this.blackNextToMove else Tile.WHITE)

        return extraBoard
    
    # check if the game is over
    def isGameOver(this, inBoard=None) -> bool:

        testBoard = this.board
        if inBoard != None:
            testBoard = inBoard

        nextCanMove = (len(this.findValidMoves(testBoard, True)) > 0)
        oppositeCanMove = (len(this.findValidMoves(testBoard, False)) > 0)

        return not (nextCanMove or oppositeCanMove)
    
    # check the margin of score
    def findMargin(this, inBoard=None) -> int:

        testBoard = this.board
        if inBoard != None:
            testBoard = inBoard

        total = 0
        for row in testBoard:
            for tile in row:
                total += tile.value # in the enum, black is -1, white is 1, and empty is 0, so they can be easily summed 

        return total

class MiniMax:

    isPlayingWhiteModifier = None
    game = None
    abPruning = None

    qualityBoard = [[4, -3, 2, 2, 2, 2, -3, 4],
                  [-3, -4, -1, -1, -1, -1, -4, -3],
                  [2, -1, 1, 0, 0, 1, -1, 2],
                  [2, -1, 0, 1, 1, 0, -1, 2],
                  [2, -1, 0, 1, 1, 0, -1, 2],
                  [2, -1, 1, 0, 0, 1, -1, 2],
                  [-3, -4, -1, -1, -1, -1, -4, -3],
                  [4, -3, 2, 2, 2, 2, -3, 4]]

    def __init__(this, color: Tile, game: Oth):
        if color == Tile.WHITE:
            this.isPlayingWhiteModifier = 1
        else:
            this.isPlayingWhiteModifier = -1
        this.game = game
        this.abPruning = True

    # minimax recursive algorithm 
    # when OthBot plays black, SAME(tryingToMaximize, inBlackNextToMove) = True
    # when OthBot plays white, SAME(tryingToMaximize, inBlackNextToMove) = False
    def minimax(this, inBoard: Matrix, depth: int, tryingToMaximize: bool, inBlackNextMove: bool, movePlayed: Position=None) -> (Position, int):
        
        # check if this position is a game over or search depth reached 
        if this.game.isGameOver(inBoard) or depth == 0:
            return ((8, 8), this.evaluateBoard(inBoard, inBlackNextMove))
        
        validMoves = this.game.findValidMoves(inBoard, inBlackNextMove)
        
        # maximize mode 
        if tryingToMaximize:
            bestEvaluation = -9999
            bestMove = None
            for position in validMoves:
                _, evaluation = this.minimax(this.game.simulateMove(inBoard, not inBlackNextMove, position, validMoves), depth - 1, False, not inBlackNextMove, position)
                bestEvaluation = max(bestEvaluation, evaluation)
                bestMove = (position if evaluation >= bestEvaluation else bestMove)
            return (bestMove, bestEvaluation)

        # minimize mode 
        else: 
            bestEvaluation = 9999
            bestMove = None
            for position in validMoves:
                _, evaluation = this.minimax(this.game.simulateMove(inBoard, not inBlackNextMove, position, validMoves), depth - 1, True, not inBlackNextMove, position)
                bestEvaluation = min(bestEvaluation, evaluation)
                bestMove = (position if evaluation <= bestEvaluation else bestMove)
            return (bestMove, bestEvaluation)

    def evaluateBoard(this, inBoard: Matrix, inBlackNextToMove: bool) -> int:

        # if this is a game over, return either positive or negative infinity based on the margin
        if this.game.isGameOver(inBoard):
            if this.game.findMargin(inBoard) > 0:
                return 9999 * this.isPlayingWhiteModifier
            elif this.game.findMargin(inBoard) < 0:
                return -9999 * this.isPlayingWhiteModifier
            else:
                return -9999 # return negative infinity on a draw, regardless of color 

        totalEvaluation = 0
        
        # first multiply the board state times the quality board
        qualitySum = this.evalQualityBoard(inBoard)
        qualitySum *= this.isPlayingWhiteModifier
        # print(f"quality sum: {qualitySum}")

        # evaluate how many moves are available to current turn
        moveMarginSum = this.evalMoveMargin(inBoard, inBlackNextToMove)
        # print(f"move margin: {moveMarginSum}")

        # evaluate how many "safe" tiles exist for black
        blackSafeSum = this.evalSafeTiles(inBoard, Tile.BLACK)
        blackSafeSum *= this.isPlayingWhiteModifier
        # print(f"black safe sum: {blackSafeSum}")

        # evaluate how many "safe" tiles exist for white
        whiteSafeSum = this.evalSafeTiles(inBoard, Tile.WHITE)
        whiteSafeSum *= this.isPlayingWhiteModifier
        # print(f"white safe sum: {whiteSafeSum}")

        totalEvaluation += qualitySum
        totalEvaluation += moveMarginSum
        totalEvaluation += blackSafeSum
        totalEvaluation += whiteSafeSum

        return totalEvaluation
    
    # evaluates heuristic based on the quality of each position in the board 
    def evalQualityBoard(this, inBoard: Matrix) -> int:
        qualityBoardSum = 0
        for i in range(len(inBoard)):
            for j in range(len(inBoard[0])):
                qualityBoardSum += inBoard[i][j].value * this.qualityBoard[i][j]

        return qualityBoardSum
    
    # eval the "freedom" of movement available on this board for the next player to move
    def evalMoveMargin(this, inBoard: Matrix, inBlackNextToMove: bool) -> int:
        moves = this.game.findValidMoves(inBoard=inBoard, inBlackNextMove=inBlackNextToMove)
        return len(moves)
    
    # find groups of safe tiles from the corners 
    def evalSafeTiles(this, inBoard: Matrix, color: Tile) -> int:

        # a "safe" group begins at the corner and covers a range on each leading edge with that color 
        # To test if a tile is safe, attempt to traverse to each direction to an edge by only passing same color tiles.
        # Each of these "safe paths" lies on an axis by which the tile can be attacked. 
        # If successful in reaching a safe path on each of the 4 axes, then the tile is safe.
        # axes are up/down, left/right, up_right/down_left, up_left/down_right
        # repeat for every tile

        totalSafe = 0

        # This dictionary holds all of the amounts to add/subtract from an index to move in a particular direction
        directions: dict = {"up": (0, -1), 
                            "up-right": (1, -1), 
                            "right": (1, 0), 
                            "down-right": (1, 1), 
                            "down": (0, 1), 
                            "down-left": (-1, 1), 
                            "left": (-1, 0), 
                            "up-left": (-1, -1)}
        
        # all positions for this color 
        thisColorPositions = this.game.findColorPositions(color, inBoard)

        for position in thisColorPositions:

            safeAxes = [False, False, False, False]

            # up/down
            (x, y) = position
            while True:
                x += directions["up"][0]
                y += directions["up"][1]
                if not this.tileIsOnBoard(x, y):
                    # success, go to the next axis 
                    safeAxes[0] = True
                    break
                elif inBoard[y][x] != color:
                    # failure, go to opposite direction
                    break
            if not safeAxes[0]:
                (x, y) = position
                while True:
                    x += directions["down"][0]
                    y += directions["down"][1]
                    if not this.tileIsOnBoard(x, y):
                        # success, go to the next axis 
                        safeAxes[0] = True
                        break
                    elif inBoard[y][x] != color:
                        # failure, go to opposite direction
                        break

            # up_right/down_left
            (x, y) = position
            while True:
                x += directions["up-right"][0]
                y += directions["up-right"][1]
                if not this.tileIsOnBoard(x, y):
                    # success, go to the next axis 
                    safeAxes[1] = True
                    break
                elif inBoard[y][x] != color:
                    # failure, go to opposite direction
                    break
            if not safeAxes[1]:
                (x, y) = position
                while True:
                    x += directions["down-left"][0]
                    y += directions["down-left"][1]
                    if not this.tileIsOnBoard(x, y):
                        # success, go to the next axis 
                        safeAxes[1] = True
                        break
                    elif inBoard[y][x] != color:
                        # failure, go to opposite direction
                        break
            
            # left/right
            (x, y) = position
            while True:
                x += directions["right"][0]
                y += directions["right"][1]
                if not this.tileIsOnBoard(x, y):
                    # success, go to the next axis 
                    safeAxes[2] = True
                    break
                elif inBoard[y][x] != color:
                    # failure, go to opposite direction
                    break
            if not safeAxes[2]:
                (x, y) = position
                while True:
                    x += directions["left"][0]
                    y += directions["left"][1]
                    if not this.tileIsOnBoard(x, y):
                        # success, go to the next axis 
                        safeAxes[2] = True
                        break
                    elif inBoard[y][x] != color:
                        # failure, go to opposite direction
                        break

            # down_right/up_left
            (x, y) = position
            while True:
                x += directions["down-right"][0]
                y += directions["down-right"][1]
                if not this.tileIsOnBoard(x, y):
                    # success, go to the next axis 
                    safeAxes[3] = True
                    break
                elif inBoard[y][x] != color:
                    # failure, go to opposite direction
                    break
            if not safeAxes[3]:
                (x, y) = position
                while True:
                    x += directions["up-left"][0]
                    y += directions["up-left"][1]
                    if not this.tileIsOnBoard(x, y):
                        # success, go to the next axis 
                        safeAxes[3] = True
                        break
                    elif inBoard[y][x] != color:
                        # failure, go to opposite direction
                        break

            if False in safeAxes:
                continue
            totalSafe += color.value

        return totalSafe

    def tileIsOnBoard(this, x: int, y: int):
        if x not in range(8) or y not in range(8):
            return False
        return True

    
class Menu:

    game = None
    bot = None
    DEBUG = False

    def __init__(this):
        this.DEBUG = False
        this.game = Oth()

    def printList(this, items: dict) -> None: 
        for i in range(len(items)):
            print(f"[{i}] {items[i]["label"]}")

    def clearConsole(this) -> None:
        os.system('cls')

    def getInput(this):
        return input(">>> ").strip()

    # entry point for the program
    def startScreen(this) -> None:

        # table of options and their functions 
        options: dict = {0: {"label": "Exit", "function": lambda: exit()}, 
                         1: {"label": "Begin two player game", "function": lambda: this.twoPlayer()}, 
                         2: {"label": "Begin bot game", "function": lambda: this.startBotPlayer()},
                         3: {"label": "Toggle debug", "function": lambda: this.toggleDebug()}}

        # menu stuff
        while True:
            invalidSelection = True
            titles = [TITLE_ASCII_ART_1, TITLE_ASCII_ART_2, TITLE_ASCII_ART_3, TITLE_ASCII_ART_4, TITLE_ASCII_ART_5]
            while invalidSelection:
                try:
                    this.clearConsole()
                    print(f"{ANSI_BACKGROUND_GREEN}{ANSI_FOREGROUND_BLACK}{titles[randrange(5)]}{ANSI_RESTORE_DEFAULT}")
                    this.printList(options)
                    userIn = int(this.getInput())
                    invalidSelection = False
                except:
                    print("That is not an integer! Please try again.")
                    input("Press enter to continue...")
                    continue 

            # run the selection 
            options[userIn]["function"]()

    # plays a move for a human
    def playCoordinate(this, inCoordinate=None) -> None:

        # printing 
        this.clearConsole()
        validMoves = this.game.findValidMoves()
        print(this.game.strWithValidMoves(validMoves))

        if len(validMoves) == 0:
            print(f"{ANSI_FOREGROUND_MAGENTA + "BLACK" if this.game.blackNextToMove else ANSI_FOREGROUND_YELLOW + "WHITE"}{ANSI_RESTORE_DEFAULT} has no valid moves and must pass.")
            input("Press enter to continue...")
            this.game.blackNextToMove = not this.game.blackNextToMove

        else:

            coordinate = None

            # human play
            if inCoordinate == None:
                print("Type the coordinate to play as a tuple like (x, y). Valid moves are highlighted yellow.")

                userIn = this.getInput()
                userIn = userIn.strip('(')
                userIn = userIn.strip(')')
                try:
                    coordinate = tuple(map(int, userIn.split(', ')))
                except:
                    print("That was not an integer tuple! Please try again.")
                    input("Press enter to continue...")
                    return

            # bot play
            else: 
                coordinate = inCoordinate

            this.game.playMove(coordinate, this.game.findValidMoves())

    def toggleDebug(this) -> None:
        this.DEBUG = not this.DEBUG
        print(f"Debug mode is now {ANSI_FOREGROUND_GREEN + "ENABLED" if this.DEBUG else ANSI_FOREGROUND_RED + "DISABLED"}{ANSI_RESTORE_DEFAULT}")
        input("Press enter to continue...")
        return 
    
    def toggleABPruning(this) -> None:
        this.bot.abPruning = not this.bot.abPruning
        print(f"AB Pruning is now {ANSI_FOREGROUND_GREEN + "ENABLED" if this.bot.abPruning else ANSI_FOREGROUND_RED + "DISABLED"}{ANSI_RESTORE_DEFAULT}")
        input("Press enter to continue...")
        return 

    # run basic game with humans
    def twoPlayer(this) -> None:

        actions = {0: {"label": "Exit", "function": lambda: exit()},
                   1: {"label": "Play move", "function": lambda: this.playCoordinate()},
                   2: {"label": "Toggle debug", "function": lambda: this.toggleDebug()}}

        # main game loop
        while not this.game.isGameOver():
            this.clearConsole()
            print(this.game)
            this.printList(actions)
            try: 
                userIn = int(this.getInput())
            except:
                print("That is not an integer! Please try again.")
                input("Press enter to continue...")
                continue
            actions[userIn]["function"]()

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

    # init a bot game
    def startBotPlayer(this) -> None:

        colors = {0: {"label": f"I want to play {ANSI_FOREGROUND_MAGENTA}BLACK{ANSI_FOREGROUND_WHITE}!", "color": Tile.WHITE},
                  1: {"label": f"I want to play {ANSI_FOREGROUND_YELLOW}WHITE{ANSI_FOREGROUND_WHITE}!", "color": Tile.BLACK}}

        while True:
            this.clearConsole()
            print("Which color do you want to play? (Black always goes first.)")
            this.printList(colors)
            userIn = None
            try: 
                userIn = int(this.getInput())
                break
            except:
                print("That is not an integer! Please try again.")
                input("Press enter to continue...")
                continue

        this.bot = MiniMax(colors[userIn]["color"], this.game)
        this.botPlayer(colors[userIn]["color"])

    # bot game loop
    def botPlayer(this, botColor: Tile) -> None:

        actions = {0: {"label": "Exit", "function": lambda: exit()},
                   1: {"label": "Play move", "function": lambda: this.playCoordinate()},
                   2: {"label": "Toggle debug", "function": lambda: this.toggleDebug()},
                   3: {"label": "Toggle AB Pruning", "function": lambda: this.toggleABPruning()}}

        # main game loop
        while not this.game.isGameOver():

            # print the board 
            this.clearConsole()
            print(this.game)

            # print bot turn, bot is black
            if this.game.blackNextToMove and botColor == Tile.BLACK:
                print("It is now OthBot's turn!")
                print("OthBot is thinking...")
                move, score = this.bot.minimax(this.game.board, SEARCH_DEPTH, True, True, None)
                print(f"OthBot wants to play {move}")
                if this.DEBUG:
                    print(f"Score of {move} is {score}")
                input("Press enter to continue...")
                this.playCoordinate(move)

            # print bot turn, bot is white
            elif not this.game.blackNextToMove and botColor == Tile.WHITE:
                print("It is now OthBot's turn!")
                print("OthBot is thinking...")
                move, score = this.bot.minimax(this.game.board, SEARCH_DEPTH, True, False, None)
                print(f"OthBot wants to play {move}")
                if this.DEBUG:
                    print(f"Score of {move} is {score}")
                input("Press enter to continue...")
                this.playCoordinate(move)

            # print human turn 
            else:
                this.printList(actions)
                try: 
                    userIn = int(this.getInput())
                except:
                    print("That is not an integer! Please try again.")
                    input("Press enter to continue...")
                    continue
                actions[userIn]["function"]()

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

if __name__ == "__main__":
    menu = Menu()
    menu.startScreen()
    # oth = Oth()
    # minimax = MiniMax(Tile.BLACK, oth)
    # print(oth.strForOutput(oth.board, True))
    # # print(f"final eval: {minimax.evaluateBoard(oth.board, True)}")
    # best = minimax.minimax(minimax.game.board, SEARCH_DEPTH, True, True)
    # print(f"Best: {best}")
    