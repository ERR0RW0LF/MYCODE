import random
from matplotlib.pylab import f
import numpy as np
from requests import get

# board is a matrix 8x8x2 with 0, 1 or 2 in each cell (0: empty, 1: white, 2: black)
# which piece is in the cell is determined by the second dimension of the matrix
# 0: none, 1: pawn, 2: knight, 3: bishop, 4: rook, 5: queen, 6: king

# the first number in a cell is the color of the piece (0: empty, 1: white, 2: black) and the second number is the type of the piece and the third is how often the piece has moved and the fourth is if a pawn has moved 2 fields in the last turn (0: no, 2: is the jumped position, 1: is the position of the pawn), the fifth is on what turn the piece has moved for the last time

board = np.array([
    [[2, 4, 0, 0, 0], [2, 2, 0, 0, 0], [2, 3, 0, 0, 0], [2, 5, 0, 0, 0], [2, 6, 0, 0, 0], [2, 3, 0, 0, 0], [2, 2, 0, 0, 0], [2, 4, 0, 0, 0]],
    [[2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 0, 0, 0]],
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
    [[1, 4, 0, 0, 0], [1, 2, 0, 0, 0], [1, 3, 0, 0, 0], [1, 5, 0, 0, 0], [1, 6, 0, 0, 0], [1, 3, 0, 0, 0], [1, 2, 0, 0, 0], [1, 4, 0, 0, 0]]
                  ])

turn = 0

# print the board in a human readable format using chess unicode characters
def print_board(board):
    print("  a b c d e f g h")
    print("  -----------------")
    for i in range(8):
        print(8 - i, end="|")
        for j in range(8):
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
def pawn_patern(board, x, y, color = 0, moved = 0):
    patern = np.zeros((8, 8))
    if color == 2:
        enemyColor = 1
    elif color == 1:
        enemyColor = 2
    else:
        return patern
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
def print_patern(patern, moves):
    print("  a b c d e f g h")
    print("  -----------------")
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
        print("|", 8 - i, end="    ")
        print(moves[i])
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
def move_piece(board, x, y, move, turn):
    pattern = get_patern(board, x, y)
    if move == 0:
        return board
    elif move > get_possible_moves(board, x, y):
        return board
    
    for i in range(8):
        for j in range(8):
            if pattern[i, j] != 0 and pattern[i, j] != 3:
                move -= 1
                if move == 0:
                    if pattern[i, j] == 5:
                        board[i, j] = board[x, y]
                        board[i, j, 3] = 1
                        board[i, j, 4] = turn
                        if pattern[i, j] == 5 and board[x, y, 0] == 1 and x == 6:
                            board[i + 1, j] = board[x, y]
                            board[i + 1, j, 3] = 2
                            board[i + 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board
                        elif pattern[i, j] == 5 and board[x, y, 0] == 2 and x == 6:
                            board[i - 1, j] = board[x, y]
                            board[i - 1, j, 3] = 2
                            board[i - 1, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board
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
                            return board
                        elif i == 7 and j == y - 2:
                            board[7, 3] = board[7, 0]
                            board[7, 3, 2] += 1
                            board[7, 3, 4] = turn
                            board[7, 0] = [0, 0, 0, 0, 0]
                            return board
                    elif pattern[i, j] == 2:
                        if board[i, j, 3] == 2:
                            if board[i, j, 0] == 1:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i - 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board
                            elif board[i, j, 0] == 2:
                                board[i, j] = board[x, y]
                                board[i, j, 3] = 1
                                board[i, j, 4] = turn
                                board[i + 1, j] = [0, 0, 0, 0, 0]
                                board[x, y] = [0, 0, 0, 0, 0]
                                return board
                        else:
                            board[i, j] = board[x, y]
                            board[i, j, 3] = 1
                            board[i, j, 4] = turn
                            board[x, y] = [0, 0, 0, 0, 0]
                            return board
                        board[i, j] = board[x, y]
                        board[i, j, 2] += 1
                        board[i, j, 4] = turn
                        board[x, y] = [0, 0, 0, 0, 0]
                    board[i, j] = board[x, y]
                    board[i, j, 2] += 1
                    board[i, j, 4] = turn
                    board[x, y] = [0, 0, 0, 0, 0]
                    return board

def random_piece(board, turn):
    movable_pieces = []
    for i in range(8):
        for j in range(8):
            if board[i, j, 0] == turn%2 + 1:
                if get_possible_moves(board, i, j) > 0:
                    movable_pieces.append((i, j))
    if len(movable_pieces) == 0:
        return None
    else:
        return movable_pieces[random.randint(0, len(movable_pieces) - 1)]

def random_move(board, x, y):
    return random.randint(0, get_possible_moves(board, x, y))





# print the board
print_board(board)
print()
print(get_patern(board, 7, 4))
print_patern(get_patern(board, 7, 4))
board[7, 5] = [0, 0, 0, 0, 0]
board[7, 6] = [0, 0, 0, 0, 0]
board[7, 3] = [0, 0, 0, 0, 0]
board[7, 2] = [0, 0, 0, 0, 0]
board[7, 1] = [0, 0, 0, 0, 0]

print()
print(get_patern(board, 6, 4))
print_patern(get_patern(board, 7, 4))
print(get_possible_moves(board, 6, 4))

print()
print_board(board=board)

print()
print(get_patern(board, 7, 4))
print_patern(get_patern(board, 7, 4))
print_board(move_piece(board, 7, 4, 2, turn=turn))
print()
print(get_patern(board, 7, 3))
print_patern(get_patern(board, 7, 3))

print()
print(board[7, 3])