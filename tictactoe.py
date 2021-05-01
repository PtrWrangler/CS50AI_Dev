"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCount = 0
    oCount = 0

    for row in board:
        for col in row:
            if col is X:
                xCount += 1
            elif col is O:
                oCount += 1

    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    availableMoves = set()

    for rIdx, row in enumerate(board):
        for cIdx, col in enumerate(row):
            if col is EMPTY:
                availableMoves.add((rIdx, cIdx))

    return availableMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tentativeBoard = copy.deepcopy(board)

    if tentativeBoard[action[0]][action[1]] is None:
        tentativeBoard[action[0]][action[1]] = player(board)

    return tentativeBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winningPlayer = None
    boardLength = len(board)

    # Check Horizontals
    for row in range(boardLength):
        if board[row][0] is not EMPTY:
            winningPlayer = board[row][0]
        else:
            continue
        for col in range(1, boardLength):
            if board[row][col] is not winningPlayer:
                winningPlayer = None
                break
        if winningPlayer is not None:
            return winningPlayer

    # Check Verticals
    for col in range(boardLength):
        if board[0][col] is not EMPTY:
            winningPlayer = board[0][col]
        else:
            continue
        for row in range(1, boardLength):
            if board[row][col] is not winningPlayer:
                winningPlayer = None
                break
        if winningPlayer is not None:
            return winningPlayer

    # Check Diagonals
    if board[0][0] is not None:
        winningPlayer = board[0][0]
    for diag in range(1, boardLength):
        if board[diag][diag] is not winningPlayer:
            winningPlayer = None
            break
    if winningPlayer is not None:
        return winningPlayer
        
    boardLengthIndex = boardLength - 1
    if board[0][boardLengthIndex] is not None:
        winningPlayer = board[0][boardLengthIndex]
    for diag in range(1, boardLength):
        if board[diag][boardLengthIndex - diag] is not winningPlayer:
            winningPlayer = None
            break
    
    return winningPlayer


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winningPlayer = winner(board)

    if winningPlayer == X:
        return 1
    elif winningPlayer == O:
        return -1
    else:
        return 0


def max_value(board):
    """
    Returns the best possible or the first optimal move for the O player
    """
    if terminal(board):
        return utility(board)

    val = -math.inf
    for action in actions(board):
        val = max(val, min_value(result(board, action)))
        if val == 1:
            return val
    return val


def min_value(board):
    """
    Returns the best possible or the first optimal move for the X player
    """
    if terminal(board):
        return utility(board)

    val = math.inf
    for action in actions(board):
        val = min(val, max_value(result(board, action)))
        if val == -1:
            return val
    return val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    boardLength = len(board)

    # If AI is first player to play, pick random move
    if board == initial_state():
        return (random.randint(0, boardLength-1), random.randint(0, boardLength-1))

    currentPlayer = player(board)

    if currentPlayer is X:
        lowestPossibleVal = -math.inf
        # for each possible move (action)
        for action in actions(board):
            # X player is looking for min possible value move
            nextMoveLowestPossibleVal = min_value(result(board, action))
            if lowestPossibleVal < nextMoveLowestPossibleVal:
                lowestPossibleVal = nextMoveLowestPossibleVal
                optimalAction = action

    elif currentPlayer is O:
        highestPossibleVal = math.inf
        # for each possible move (action)
        for action in actions(board):
            # O player is looking for max possible value move
            nextMoveHighestPossibleVal = max_value(result(board, action))
            if highestPossibleVal > nextMoveHighestPossibleVal:
                highestPossibleVal = nextMoveHighestPossibleVal
                optimalAction = action

    return optimalAction