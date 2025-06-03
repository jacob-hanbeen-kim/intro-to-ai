"""
Tic Tac Toe Player
"""
import copy
import math
import random

from sphinx.cmd.quickstart import nonempty

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
    numX = 0
    numO = 0
    for row in board:
        for space in row:
            if space == O:
                numO += 1
            elif space == X:
                numX += 1

    if numX == numO:
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action.")

    updatedBoard = copy.deepcopy(board)
    updatedBoard[action[0]][action[1]] = player(board)

    return updatedBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # all(i == board[0][0] for i in board[0])
    winning_combinations = [
        # rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(2, 0), (1, 1), (0, 2)]
    ]

    for combination in winning_combinations:
        one, two, three = combination
        if board[one[0]][one[1]] == board[two[0]][two[1]] == board[three[0]][three[1]] != EMPTY:
            return board[one[0]][one[1]]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O or len(actions(board)) == 0:
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        val, action = max(board)
    else:
        val, action = min(board)

    return action

def min(board):
    if terminal(board):
        return utility(board), None

    minimum = float("inf")
    moveMade = None

    for action in actions(board):
        val, act = max(result(board, action))
        if val < minimum:
            minimum = val
            moveMade = action

    return minimum, moveMade

def max(board):
    if terminal(board):
        return utility(board), None

    maximum = float("-inf")
    moveMade = None

    for action in actions(board):
        val, act = min(result(board, action))
        if val > maximum:
            maximum = val
            moveMade = action

    return maximum, moveMade



def random_agent(board):
    """
    Returns a random action from the available actions left on the board
    """
    possibleActions = actions(board)
    if possibleActions:
        return random.choice(list(possibleActions))
    else:
        return None