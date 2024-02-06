import random
import numpy as np

# board is a matrix 8x8x2 with 0, 1 or 2 in each cell (0: empty, 1: white, 2: black)
# which piece is in the cell is determined by the second dimension of the matrix
# 0: none, 1: pawn, 2: knight, 3: bishop, 4: rook, 5: queen, 6: king

board = np.array([
    [[2, 4], [2, 2], [2, 3], [2, 5], [2, 6], [2, 3], [2, 2], [2, 4]],
    [[2, 1], [2, 1], [2, 1], [2, 1], [2, 1], [2, 1], [2, 1], [2, 1]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
    [[1, 4], [1, 2], [1, 3], [1, 5], [1, 6], [1, 3], [1, 2], [1, 4]]
                  ])

# print the board in a human readable format using chess unicode characters
def print_board(board):
    print("  a b c d e f g h")
    print("  -----------------")
    for i in range(8):
        print(8 - i, end="|")
        for j in range(8):
            if board[i, j, 0] == 0:
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
# 0 can't move there, 1 can move there, 2 can move there and take a piece, 3 is possicion of the piece

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
def king_patern(board, x, y, color = 0):
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
    return patern

# print paterns readable
def print_patern(patern):
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
        print("|", 8 - i)
    print("  -----------------")
    print("  a b c d e f g h")


# print the board
print_board(board)
print(bishop_patern(board, 3, 3, 2))
print(knight_patern(board, 3, 3, 2))
print_patern(pawn_patern(board, 3, 3, 2))