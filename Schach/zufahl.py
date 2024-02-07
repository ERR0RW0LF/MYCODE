from hmac import new
from math import e, log
import random
from matplotlib.pyplot import pie
import numpy as np
import logging
import time

# board is a matrix 8x8x2 with 0, 1 or 2 in each cell (0: empty, 1: white, 2: black)
# which piece is in the cell is determined by the second dimension of the matrix
# 0: none, 1: pawn, 2: knight, 3: bishop, 4: rook, 5: queen, 6: king

# the first number in a cell is the color of the piece (0: empty, 1: white, 2: black) and the second number is the type of the piece and the third is how often the piece has moved and the fourth is if a pawn has moved 2 fields in the last turn (0: no, 2: is the jumped position, 1: is the position of the pawn), the fifth is on what turn the piece has moved for the last time
board_base = np.array([
    [
        [2, 4, 0, 0, 0], [2, 2, 0, 0, 0], [2, 3, 0, 0, 0], [2, 5, 0, 0, 0], [2, 6, 0, 0, 0], [2, 3, 0, 0, 0], [2, 2, 0, 0, 0], [2, 4, 0, 0, 0]
    ],
    [
        [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    ],
    [
        [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]
    ],
    [
        [1, 4, 0, 0, 0], [1, 2, 0, 0, 0], [1, 3, 0, 0, 0], [1, 5, 0, 0, 0], [1, 6, 0, 0, 0], [1, 3, 0, 0, 0], [1, 2, 0, 0, 0], [1, 4, 0, 0, 0]
    ]
                  ])

movesY = ["a", "b", "c", "d", "e", "f", "g", "h"]

movement = []


# print the board in a human readable format using chess unicode characters
def print_board(board, last_move, turn):
    """
    Prints the chess board with the current state of the game.

    Args:
        board (numpy.ndarray): The chess board represented as a 3D numpy array.
        last_move (str): The last move made in algebraic notation.
        turn (int): The current turn number.

    Returns:
        None

    Prints the chess board with the pieces represented by unicode characters.
    The board is printed with row numbers and column letters for reference.
    The last move and turn number are also displayed.

    Example:
        >>> board = np.zeros((8, 8, 4))
        >>> last_move = "e2e4"
        >>> turn = 1
        >>> print_board(board, last_move, turn)
          a b c d e f g h
          ----------------
        8|r n b q k b n r|
        7|p p p p p p p p|
        6|              |
        5|              |
        4|        P     |
        3|              |
        2|P P P P   P P P|
        1|R N B Q K B N R|
          ----------------
          a b c d e f g h
        Turn: 1
    """
    # Function implementation goes here
    if turn != 0:
        delete_last_lines(15)
    if len(last_move) > 0:
        print("Last move: ", last_move)
    
    print()
    print("  a b c d e f g h")
    print("  ----------------")
    for i in range(8):
        print(str(8 - i), end="|")
        for j in range(8):
            #logging.info(board[i, j])
            if board[i, j, 0] == 0:
                print(" ", end=" ")
            elif board[i, j, 3] == 2:
                print(" ", end=" ")
            elif board[i, j, 0] == 2:
                if board[i, j, 1] == 1:
                    print("\u2659", end=" ")
                elif board[i, j, 1] == 2:
                    print("\u2658", end=" ")
                elif board[i, j, 1] == 3:
                    print("\u2657", end=" ")
                elif board[i, j, 1] == 4:
                    print("\u2656", end=" ")
                elif board[i, j, 1] == 5:
                    print("\u2655", end=" ")
                elif board[i, j, 1] == 6:
                    print("\u2654", end=" ")
            elif board[i, j, 0] == 1:
                if board[i, j, 1] == 1:
                    print("\u265F", end=" ")
                elif board[i, j, 1] == 2:
                    print("\u265E", end=" ")
                elif board[i, j, 1] == 3:
                    print("\u265D", end=" ")
                elif board[i, j, 1] == 4:
                    print("\u265C", end=" ")
                elif board[i, j, 1] == 5:
                    print("\u265B", end=" ")
                elif board[i, j, 1] == 6:
                    print("\u265A", end=" ")
        print("|", 8 - i)
    print("  ----------------")
    print("  a b c d e f g h")
    print("Turn: ", turn)

# q: how can i print something in the console next to something else without a new line?
# a: use the end parameter in the print function
# q: how does the end parameter work?
# a: the end parameter is the last character of the printed string
# paterns for each piece
# 0 can't move there, 1 can move there, 2 can move there and take a piece, 3 is position of the piece, 4 (for the king) Castling position, 5 (for the pawn) en passant position

# bishop patern
def bishop_patern(board, x, y, color=0):
    """
    Generates a pattern for a bishop piece on a chessboard.

    Args:
        board (numpy.ndarray): The chessboard represented as a 3D numpy array.
        x (int): The x-coordinate of the bishop's position on the board.
        y (int): The y-coordinate of the bishop's position on the board.
        color (int, optional): The color of the bishop. Defaults to 0.

    Returns:
        numpy.ndarray: A 2D numpy array representing the bishop's movement pattern.
            - 0: Empty square
            - 1: Valid move
            - 2: Capture move
            - 3: Bishop's current position

    """
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    patern[x, y] = 3
    for i in range(1, 8):
        if x + i < 8 and y + i < 8:
            if board[x + i, y + i, 0] == 0:
                patern[x + i, y + i] = 1
            elif board[x + i, y + i, 0] == enemyColor:
                patern[x + i, y + i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y - i >= 0:
            if board[x - i, y - i, 0] == 0:
                patern[x - i, y - i] = 1
            elif board[x - i, y - i, 0] == enemyColor:
                patern[x - i, y - i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x + i < 8 and y - i >= 0:
            if board[x + i, y - i, 0] == 0:
                patern[x + i, y - i] = 1
            elif board[x + i, y - i, 0] == enemyColor:
                patern[x + i, y - i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y + i < 8:
            if board[x - i, y + i, 0] == 0:
                patern[x - i, y + i] = 1
            elif board[x - i, y + i, 0] == enemyColor:
                patern[x - i, y + i] = 2
                break
            else:
                break
        else:
            break
    return patern

# knight patern
def knight_patern(board, x, y, color = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    
    patern[x, y] = 3
    
    for i in range(1, 8):
        if x + i < 8 and y + 2 < 8:
            if board[x + i, y + 2, 0] == 0:
                patern[x + i, y + 2] = 1
            elif board[x + i, y + 2, 0] == enemyColor:
                patern[x + i, y + 2] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x + i < 8 and y - 2 >= 0:
            if board[x + i, y - 2, 0] == 0:
                patern[x + i, y - 2] = 1
            elif board[x + i, y - 2, 0] == enemyColor:
                patern[x + i, y - 2] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y + 2 < 8:
            if board[x - i, y + 2, 0] == 0:
                patern[x - i, y + 2] = 1
            elif board[x - i, y + 2, 0] == enemyColor:
                patern[x - i, y + 2] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y - 2 >= 0:
            if board[x - i, y - 2, 0] == 0:
                patern[x - i, y - 2] = 1
            elif board[x - i, y - 2, 0] == enemyColor:
                patern[x - i, y - 2] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x + 2 < 8 and y + i < 8:
            if board[x + 2, y + i, 0] == 0:
                patern[x + 2, y + i] = 1
            elif board[x + 2, y + i, 0] == enemyColor:
                patern[x + 2, y + i] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x + 2 < 8 and y - i >= 0:
            if board[x + 2, y - i, 0] == 0:
                patern[x + 2, y - i] = 1
            elif board[x + 2, y - i, 0] == enemyColor:
                patern[x + 2, y - i] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x - 2 >= 0 and y + i < 8:
            if board[x - 2, y + i, 0] == 0:
                patern[x - 2, y + i] = 1
            elif board[x - 2, y + i, 0] == enemyColor:
                patern[x - 2, y + i] = 2
            break
        else:
            break
    for i in range(1, 8):
        if x - 2 >= 0 and y - i >= 0:
            if board[x - 2, y - i, 0] == 0:
                patern[x - 2, y - i] = 1
            elif board[x - 2, y - i, 0] == enemyColor:
                patern[x - 2, y - i] = 2
            break
        else:
            break
    return patern

# rook patern
def rook_patern(board, x, y, color = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    patern[x, y] = 3
    for i in range(1, 8):
        if x + i < 8:
            if board[x + i, y, 0] == 0:
                patern[x + i, y] = 1
            elif board[x + i, y, 0] == enemyColor:
                patern[x + i, y] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0:
            if board[x - i, y, 0] == 0:
                patern[x - i, y] = 1
            elif board[x - i, y, 0] == enemyColor:
                patern[x - i, y] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if y + i < 8:
            if board[x, y + i, 0] == 0:
                patern[x, y + i] = 1
            elif board[x, y + i, 0] == enemyColor:
                patern[x, y + i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if y - i >= 0:
            if board[x, y - i, 0] == 0:
                patern[x, y - i] = 1
            elif board[x, y - i, 0] == enemyColor:
                patern[x, y - i] = 2
                break
            else:
                break
        else:
            break
    return patern

# queen patern
def queen_patern(board, x, y, color = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    patern[x, y] = 3
    for i in range(1, 8):
        if x + i < 8:
            if board[x + i, y, 0] == 0:
                patern[x + i, y] = 1
            elif board[x + i, y, 0] == enemyColor:
                patern[x + i, y] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0:
            if board[x - i, y, 0] == 0:
                patern[x - i, y] = 1
            elif board[x - i, y, 0] == enemyColor:
                patern[x - i, y] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if y + i < 8:
            if board[x, y + i, 0] == 0:
                patern[x, y + i] = 1
            elif board[x, y + i, 0] == enemyColor:
                patern[x, y + i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if y - i >= 0:
            if board[x, y - i, 0] == 0:
                patern[x, y - i] = 1
            elif board[x, y - i, 0] == enemyColor:
                patern[x, y - i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x + i < 8 and y + i < 8:
            if board[x + i, y + i, 0] == 0:
                patern[x + i, y + i] = 1
            elif board[x + i, y + i, 0] == enemyColor:
                patern[x + i, y + i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y - i >= 0:
            if board[x - i, y - i, 0] == 0:
                patern[x - i, y - i] = 1
            elif board[x - i, y - i, 0] == enemyColor:
                patern[x - i, y - i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x + i < 8 and y - i >= 0:
            if board[x + i, y - i, 0] == 0:
                patern[x + i, y - i] = 1
            elif board[x + i, y - i, 0] == enemyColor:
                patern[x + i, y - i] = 2
                break
            else:
                break
        else:
            break
    for i in range(1, 8):
        if x - i >= 0 and y + i < 8:
            if board[x - i, y + i, 0] == 0:
                patern[x - i, y + i] = 1
            elif board[x - i, y + i, 0] == enemyColor:
                patern[x - i, y + i] = 2
                break
            else:
                break
        else:
            break
    return patern

# king patern
def king_patern(board, x, y, color = 0, moved = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    patern[x, y] = 3
    if x + 1 < 8:
        if board[x + 1, y, 0] == 0:
            patern[x + 1, y] = 1
        elif board[x + 1, y, 0] == enemyColor:
            patern[x + 1, y] = 2
    if x - 1 >= 0:
        if board[x - 1, y, 0] == 0:
            patern[x - 1, y] = 1
        elif board[x - 1, y, 0] == enemyColor:
            patern[x - 1, y] = 2
    if y + 1 < 8:
        if board[x, y + 1, 0] == 0:
            patern[x, y + 1] = 1
        elif board[x, y + 1, 0] == enemyColor:
            patern[x, y + 1] = 2
    if y - 1 >= 0:
        if board[x, y - 1, 0] == 0:
            patern[x, y - 1] = 1
        elif board[x, y - 1, 0] == enemyColor:
            patern[x, y - 1] = 2
    if x + 1 < 8 and y + 1 < 8:
        if board[x + 1, y + 1, 0] == 0:
            patern[x + 1, y + 1] = 1
        elif board[x + 1, y + 1, 0] == enemyColor:
            patern[x + 1, y + 1] = 2
    if x - 1 >= 0 and y - 1 >= 0:
        if board[x - 1, y - 1, 0] == 0:
            patern[x - 1, y - 1] = 1
        elif board[x - 1, y - 1, 0] == enemyColor:
            patern[x - 1, y - 1] = 2
    if x + 1 < 8 and y - 1 >= 0:
        if board[x + 1, y - 1, 0] == 0:
            patern[x + 1, y - 1] = 1
        elif board[x + 1, y - 1, 0] == enemyColor:
            patern[x + 1, y - 1] = 2
    if x - 1 >= 0 and y + 1 < 8:
        if board[x - 1, y + 1, 0] == 0:
            patern[x - 1, y + 1] = 1
        elif board[x - 1, y + 1, 0] == enemyColor:
            patern[x - 1, y + 1] = 2
    if moved == 0:
        if color == 1:
            if board[7, 5, 0] == 0 and board[7, 6, 0] == 0 and board[7, 7, 1] == 4 and board[7, 7, 2] == 0:
                patern[7, 6] = 4
            if board[7, 3, 0] == 0 and board[7, 2, 0] == 0 and board[7, 0, 1] == 4 and board[7, 0, 2] == 0:
                patern[7, 2] = 4
        elif color == 2:
            if board[0, 5, 0] == 0 and board[0, 6, 0] == 0 and board[0, 7, 1] == 4 and board[0, 7, 2] == 0:
                patern[0, 6] = 4
            if board[0, 3, 0] == 0 and board[0, 2, 0] == 0 and board[0, 0, 1] == 4 and board[0, 0, 2] == 0:
                patern[0, 2] = 4
                
    return patern

# pawn patern
def pawn_patern(board, x, y, color = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
    moved = board[x, y, 2]
    patern[x, y] = 3
    if color == 1:
        if x - 1 >= 0:
            if y - 1 >= 0:
                if board[x - 1, y - 1, 0] == enemyColor:
                    patern[x - 1, y - 1] = 2
            if y + 1 < 8:
                if board[x - 1, y + 1, 0] == enemyColor:
                    patern[x - 1, y + 1] = 2
            if board[x - 1, y, 0] == 0:
                patern[x - 1, y] = 1
            if x == 6 and board[x - 2, y, 0] == 0:
                patern[x - 2, y] = 1
            if moved == 0:
                if board[x - 1, y, 0] == 0 and board[x - 2, y, 0] == 0:
                    patern[x - 2, y] = 5
                    patern[x - 1, y] = 1
    elif color == 2:
        if x + 1 < 8:
            if y - 1 >= 0:
                if board[x + 1, y - 1, 0] == enemyColor:
                    patern[x + 1, y - 1] = 2
            if y + 1 < 8:
                if board[x + 1, y + 1, 0] == enemyColor:
                    patern[x + 1, y + 1] = 2
            if board[x + 1, y, 0] == 0:
                patern[x + 1, y] = 1
            if x == 1 and board[x + 2, y, 0] == 0:
                patern[x + 2, y] = 1
            if moved == 0:
                if board[x + 1, y, 0] == 0 and board[x + 2, y, 0] == 0:
                    patern[x + 2, y] = 5
                    patern[x + 1, y] = 1
    return patern

# promote a pawn
def promote_pawn(board, x, y, color, piece):
    if color == 1:
        if x == 0:
            board[x, y, 1] = piece
    elif color == 2:
        if x == 7:
            board[x, y, 1] = piece
    return board

# promote to random piece
def promote_pawn_random(board, x, y, color):
    if color == 1:
        if x == 0:
            board[x, y, 1] = random.randint(2, 5)
            board[x, y, 2] = 0
            board[x, y, 3] = 0
            board[x, y, 4] = 0
    elif color == 2:
        if x == 7:
            board[x, y, 1] = random.randint(2, 5)
            board[x, y, 2] = 0
            board[x, y, 3] = 0
            board[x, y, 4] = 0
    return board

# print paterns readable
def print_patern(patern):
    print("  a b c d e f g h")
    print("  -----------------")
    if type(patern) == list:
        for i in range(8):
            print(8 - i, end="|")
            for j in range(8):
                if patern[i, j] == 0:
                    print(" ", end=" ")
                elif patern[i, j] == 1:
                    print("o", end=" ")
                elif patern[i, j] == 2:
                    print("x", end=" ")
                elif patern[i, j] == 3:
                    print("P", end=" ")
                elif patern[i, j] == 4:
                    print("C", end=" ")
                elif patern[i, j] == 5:
                    print("E", end=" ")
            print("|", 8 - i)
    else:
        for i in range(8):
            print(8 - i, end="|")
            for j in range(8):
                print(" ", end=" ")
            print("|", 8 - i)
    print("  -----------------")
    print("  a b c d e f g h")

# get number of all possible moves for a piece on the board
def get_possible_moves(board, x, y):
    if board[x, y, 1] == 1:
        patern = pawn_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 2:
        patern = knight_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 3:
        patern = bishop_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 4:
        patern = rook_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 5:
        patern = queen_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 6:
        patern = king_patern(board, x, y, board[x, y, 0], board[x, y, 2])
    return np.count_nonzero(patern) - 1

# get the patern for a piece on the board
def get_patern(board, x, y):
    if board[x, y, 1] == 1:
        return pawn_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 2:
        return knight_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 3:
        return bishop_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 4:
        return rook_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 5:
        return queen_patern(board, x, y, board[x, y, 0])
    elif board[x, y, 1] == 6:
        return king_patern(board, x, y, board[x, y, 0], moved=board[x, y, 2])

# move a piece on the board based on the patern and the number of the move (0 is the original position, 1 is the first possible position in the patern from left to right and up to down, 2 is the second possible position, ...) and return the new board
def move_piece(board, x, y, move, turn, moves: list):
    pattern = get_patern(board, x, y)
    last_move = ""
    if move == 0:
        return board, moves, last_move
    elif move > get_possible_moves(board, x, y):
        return board, moves, last_move
    
    for i in range(8):
        for j in range(8):
            if pattern[i, j] != 0 and pattern[i, j] != 3:
                move -= 1
                logging.info("Move: " + str(move))
                if move == 0:
                    logging.info("Move: " + str(move))
                    if board[x, y, 1] == 1:
                        zug = 'P ' + str(movesY[y]) + str(8 - x) + ' to ' + str(movesY[j]) + str(8 - i)
                    elif board[x, y, 1] == 2:
                        zug = 'K ' + str(movesY[y]) + str(8 - x) + ' takes ' + str(movesY[j]) + str(8 - i)
                    elif board[x, y, 1] == 3:
                        zug = 'B ' + str(movesY[y]) + str(8 - x) + ' takes ' + str(movesY[j]) + str(8 - i)
                    elif board[x, y, 1] == 4:
                        zug = 'R ' + str(movesY[y]) + str(8 - x) + ' takes ' + str(movesY[j]) + str(8 - i)
                    elif board[x, y, 1] == 5:
                        zug = 'Q ' + str(movesY[y]) + str(8 - x) + ' takes ' + str(movesY[j]) + str(8 - i)
                    elif board[x, y, 1] == 6:
                        zug = 'K ' + str(movesY[y]) + str(8 - x) + ' takes ' + str(movesY[j]) + str(8 - i)
                    logging.info(zug)
                    logging.info(moves)
                    if len(moves) > 0:
                        moves.append(zug)
                        movement = moves
                        logging.info(1)
                    elif moves != []:
                        moves.append(zug)
                        movement = moves
                        logging.info(1)
                    else:
                        movement = [zug]
                        logging.info(2)
                    logging.info(movement)
                    last_move = zug
                    if pattern[i, j] == 5:
                        board[i, j] = board[x, y]
                        board[i, j, 3] = 1
                        board[i, j, 4] = turn
                        if pattern[i, j] == 5 and board[x, y, 0] == 1 and x == 6:
                            board[i + 1, j] = board[x, y]
                            board[i + 1, j, 3] = 2
                            board[i + 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board, movement, last_move
                        elif pattern[i, j] == 5 and board[x, y, 0] == 2 and x == 6:
                            board[i - 1, j] = board[x, y]
                            board[i - 1, j, 3] = 2
                            board[i - 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board, movement, last_move
                    elif pattern[i, j] == 4:
                        board[i, j] = board[x, y]
                        board[i, j, 2] += 1
                        board[i, j, 4] = turn
                        board[x, y] = [0, 0, 0, 0, 0]
                        if i == 7 and j == y + 2:
                            board[7, 5] = board[7, 7]
                            board[7, 5, 2] += 1
                            board[7, 5, 4] = turn
                            board[7, 7] = [0, 0, 0, 0, 0]
                            return board, movement, last_move
                        elif i == 7 and j == y - 2:
                            board[7, 3] = board[7, 0]
                            board[7, 3, 2] += 1
                            board[7, 3, 4] = turn
                            board[7, 0] = [0, 0, 0, 0, 0]
                            return board, movement, last_move
                    elif pattern[i, j] == 2:
                        if board[i, j, 3] == 2:
                            if board[i, j, 0] == 1:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i - 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board, movement, last_move
                            elif board[i, j, 0] == 2:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i + 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board, movement, last_move
                        else:
                            board[i, j] = board[x, y]
                            board[i, j, 3] = 1
                            board[i, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            if board[i, j, 1] == 1:
                                board = promote_pawn_random(board, i, j, board[i, j, 0])
                            return board, movement, last_move
                        board[i, j] = board[x, y]
                        board[i, j, 2] += 1
                        board[i, j, 4] = turn
                        if board[i, j, 1] == 1:
                            board = promote_pawn_random(board, i, j, board[i, j, 0])
                        board[x, y] = [0, 0, 0, 0, 0]
                    board[i, j] = board[x, y]
                    board[i, j, 2] += 1
                    board[i, j, 4] = turn
                    if board[i, j, 1] == 1:
                        board = promote_pawn_random(board, i, j, board[i, j, 0])
                    board[x, y] = [0, 0, 0, 0, 0]
                    return board, movement, last_move

def random_piece(board, turn):
    
    movable_pieces = []
    for i in range(8):
        for j in range(8):
            if board[i, j, 0] == (int(turn) % 2) + 1:
                if get_possible_moves(board, i, j) > 0:
                    movable_pieces.append((i, j))
    if len(movable_pieces) == 0:
        return None
    else:
        return movable_pieces[random.randint(0, len(movable_pieces) - 1)]

def random_move(board, x, y):
    return random.randint(0, get_possible_moves(board, x, y) - 1)

# determine the winner of the game
def get_winner(board):
    pieces = 0
    wight_king = False
    black_king = False
    can_move_white = False
    can_move_black = False
    for i in range(8):
        for j in range(8):
            pieces = 0
            if board[i, j, 1] == 6 and board[i, j, 0] == 1:
                wight_king = True
            if board[i, j, 1] == 6 and board[i, j, 0] == 2:
                black_king = True
            if board[i, j, 0] == 0:
                continue
            
    if wight_king == False and black_king == False:
        return 3
    if wight_king == True and black_king == False:
        return 1
    if wight_king == False and black_king == True:
        return 2
    if wight_king == True and black_king == True:
        return 0
    return 0
# q: what are the outputs of the get_winner function?
# a: 0 is no winner, 1 is white wins, 2 is black wins, 3 is draw

# readable winner
def readable_winner(winner):
    if winner == 0:
        return "No winner"
    elif winner == 1:
        return "White wins"
    elif winner == 2:
        return "Black wins"
    elif winner == 3:
        return "Draw"

# round 
def round(board, turn, moves):
    new_board = np.array(board)
    # q: how can i check if two numpy arrays with 3 dimensions are equal?
    # a: np.array_equal(array1, array2)
    
    piece = random_piece(board, turn)
    if piece == None:
        return board, turn, moves, ""
    move = random_move(board, piece[0], piece[1])
    move_out = move_piece(board, piece[0], piece[1], move, turn, moves)
    new_board = np.array(move_out[0])
    moves = move_out[1]
    last_move = move_out[2]
    board = new_board
    return board, turn + 1, moves, last_move

# main function
def main(board, turn: int, moves):
    print('\n' * 15)
    while get_winner(board) == 0:
        old_turn = turn
        board, turn, moves, last_move = round(board, turn, moves)
        if old_turn == turn or last_move == "":
            continue
        else:
            print_board(board, last_move, turn)
            time.sleep(0.01)
    print("Winner: ", readable_winner(get_winner(board)))
    print("Moves: ")
    for i in moves:
        print(i)
    print(turn)
    winner = get_winner(board)
    return board, turn, moves, winner

# overwrite the board with the new board in the terminal
def delete_last_lines(n=1):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE, end='')


# print the board
#print_board(board, moves=movement, turn=turn)
##print()
##print(get_patern(board, 7, 4))
##print_patern(get_patern(board, 7, 4))
#'''board[7, 5] = [0, 0, 0, 0, 0]
#board[7, 6] = [0, 0, 0, 0, 0]
#board[7, 3] = [0, 0, 0, 0, 0]
#board[7, 2] = [0, 0, 0, 0, 0]
#board[7, 1] = [0, 0, 0, 0, 0]'''
#
##print()
##print(get_patern(board, 6, 4))
##print_patern(get_patern(board, 7, 4))
##print(get_possible_moves(board, 6, 4))
#
#print()
#print_board(board=board, moves=movement, turn=turn)
#
#print()
##print(get_patern(board, 7, 4))
##print_patern(get_patern(board, 7, 4))
#
#board, movement = move_piece(board, 6, 4, 1, turn=turn, moves=movement)
#
#print_board(board, moves=movement, turn=turn)
#print()
##print(get_patern(board, 7, 3))
##print_patern(get_patern(board, 7, 3))
#
##print()
#print(board[7, 3])

# q: what levels of logging are there?
# a: DEBUG, INFO, WARNING, ERROR, CRITICAL
# q: what is the difference between the levels of logging?
# a: DEBUG is for debugging, INFO is for information, WARNING is for warnings, ERROR is for errors, CRITICAL is for critical errors

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logging.info('Started')
    logging.info('Imported modules')
    logging.info('Starting the game')
    turn = 0
    board = board_base
    winnes = []
    turns = []
    
    
    for i in range(100):
        board, turn, movement, winner = main(board, turn, [])
        winnes.append(winner)
        turns.append(turn)
        board = board_base
        turn = 0
        print("Game: ", i + 1)
    
    winnesW = 0
    winnesB = 0
    winnesD = 0
    for i in winnes:
        if i == 1:
            winnesW += 1
        elif i == 2:
            winnesB += 1
        elif i == 3:
            winnesD += 1
    
    print("White wins: ", winnesW)
    print("Black wins: ", winnesB)
    print("Draws: ", winnesD)
    print("Average turns: ", sum(turns) / len(turns))
    
    print("White wins: ", winnesW / len(winnes) * 100, "%")
    print("Black wins: ", winnesB / len(winnes) * 100, "%")
    print("Draws: ", winnesD / len(winnes) * 100, "%")
    
    #main(board, turn, movement)
    
    print('\u2654')
    print('\u265A')
    
    #board = board_base
    #main(board, turn, movement)