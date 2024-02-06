from math import e, log
import random
from matplotlib.pylab import f
import numpy as np
from requests import get
from torch import NoneType, rand
import logging

# board is a matrix 8x8x2 with 0, 1 or 2 in each cell (0: empty, 1: white, 2: black)
# which piece is in the cell is determined by the second dimension of the matrix
# 0: none, 1: pawn, 2: knight, 3: bishop, 4: rook, 5: queen, 6: king

# the first number in a cell is the color of the piece (0: empty, 1: white, 2: black) and the second number is the type of the piece and the third is how often the piece has moved and the fourth is if a pawn has moved 2 fields in the last turn (0: no, 2: is the jumped position, 1: is the position of the pawn), the fifth is on what turn the piece has moved for the last time
board = np.array([
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
def print_board(board, moves, turn):
    if len(moves) > 0:
        for m in moves:
            print(m, end=" ")
    elif moves != None:
        for m in moves:
            print(m, end=" ")
    print()
    print("  a b c d e f g h")
    print("  -----------------")
    for i in range(8):
        print(8 - i, end="|")
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
    print("  -----------------")
    print("  a b c d e f g h")
    print("Turn: ", turn)

# q: how can i print something in the console next to something else without a new line?
# a: use the end parameter in the print function
# q: how does the end parameter work?
# a: the end parameter is the last character of the printed string
# paterns for each piece
# 0 can't move there, 1 can move there, 2 can move there and take a piece, 3 is position of the piece, 4 (for the king) Castling position, 5 (for the pawn) en passant position

# bishop patern
def bishop_patern(board, x, y, color = 0):
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
    if move == 0:
        return board, moves
    elif move > get_possible_moves(board, x, y):
        return board, moves
    
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
                    if pattern[i, j] == 5:
                        board[i, j] = board[x, y]
                        board[i, j, 3] = 1
                        board[i, j, 4] = turn
                        if pattern[i, j] == 5 and board[x, y, 0] == 1 and x == 6:
                            board[i + 1, j] = board[x, y]
                            board[i + 1, j, 3] = 2
                            board[i + 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board, movement
                        elif pattern[i, j] == 5 and board[x, y, 0] == 2 and x == 6:
                            board[i - 1, j] = board[x, y]
                            board[i - 1, j, 3] = 2
                            board[i - 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board, movement
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
                            return board, movement
                        elif i == 7 and j == y - 2:
                            board[7, 3] = board[7, 0]
                            board[7, 3, 2] += 1
                            board[7, 3, 4] = turn
                            board[7, 0] = [0, 0, 0, 0, 0]
                            return board, movement
                    elif pattern[i, j] == 2:
                        if board[i, j, 3] == 2:
                            if board[i, j, 0] == 1:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i - 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board, movement
                            elif board[i, j, 0] == 2:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i + 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board, movement
                        else:
                            board[i, j] = board[x, y]
                            board[i, j, 3] = 1
                            board[i, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board, movement
                        board[i, j] = board[x, y]
                        board[i, j, 2] += 1
                        board[i, j, 4] = turn
                        board[x, y] = [0, 0, 0, 0, 0]
                    board[i, j] = board[x, y]
                    board[i, j, 2] += 1
                    board[i, j, 4] = turn
                    board[x, y] = [0, 0, 0, 0, 0]
                    return board, movement

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
    for i in range(8):
        for j in range(8):
            if board[i, j, 1] == 6 and board[i, j, 0] == 1:
                for k in range(8):
                    for l in range(8):
                        if board[k, l, 0] == 2:
                            if get_possible_moves(board, k, l) > 0:
                                return 0
                return 1
            if board[i, j, 1] == 6 and board[i, j, 0] == 2:
                for k in range(8):
                    for l in range(8):
                        if board[k, l, 0] == 1:
                            if get_possible_moves(board, k, l) > 0:
                                return 0
                return 2
    return 0
# q: what are the outputs of the get_winner function?
# a: 0 is no winner, 1 is white wins, 2 is black wins

# round 
def round(board, turn, moves):
    
    piece = random_piece(board, turn)
    if piece == None:
        return board, turn, moves
    move = random_move(board, piece[0], piece[1])
    move_out = move_piece(board, piece[0], piece[1], move, turn, moves)
    board = move_out[0]
    moves = move_out[1]
    return board, turn + 1, moves

# main function
def main(board, turn: int, moves):
    
    while get_winner(board) == 0:
        board, turn, moves = round(board, turn, moves)
        print_board(board, moves, turn)
    print("Winner: ", get_winner(board))
    print("Moves: ", moves)
    return board, turn, moves


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

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    logging.info('Imported modules')
    logging.info('Starting the game')
    turn = 0
    seed = 0
    random.seed(seed)
    main(board, turn, movement)