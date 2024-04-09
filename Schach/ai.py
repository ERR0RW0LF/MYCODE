import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.utils.data as data
from torch.utils.data import DataLoader
import logging
import time
import os
import sys


# the framework will be pytorch
# the ai will be a convolutional neural network
# The ai will be rl based and will use a neural network to predict the best move
# the neural network will be trained using reinforcement learning
# the ai will be able to play against itself to train itself
# the ai will be able to play against a human player
# the board will be represented as a 8x8x5 matrix
# the first dimension will be the color of the piece (0: empty, 1: white, 2: black)
# the second dimension will be the type of the piece (0: none, 1: pawn, 2: knight, 3: bishop, 4: rook, 5: queen, 6: king)
# the third dimension will be how often the piece has moved
# the fourth dimension will be if a pawn has moved 2 fields in the last turn (0: no, 2: is the jumped position, 1: is the position of the pawn)
# the fifth dimension will be on what turn the piece has moved for the last time

# the ai will be a class with the following methods:
# __init__(): initializes the ai
# move(): makes a move if it is valid and returns the reward else returns a negative reward
# train(): trains the ai
# play(): lets the ai play against a human player
# predict(): predicts the best move for the ai
# save(): saves the ai to a file
# load(): loads the ai from a file

# if a move is valid is will be checked before it is executed
# if a move is invalid the ai will be given a negative reward and the move will be repeated

# q: how do i create a neural network in pytorch that can predict the best move for a given board and is trained using reinforcement learning?
# a: i will create a class ai with the following methods: __init__(), train(), play(), predict(), save(), load()
# the ai will be a convolutional neural network with 5 layers
# the input layer will have 8x8x5 neurons
# the first hidden layer will have 128 neurons
# the second hidden layer will have 64 neurons
# the third hidden layer will have 32 neurons
# the fourth hidden layer will have 16 neurons
# the output layer will have 64 neurons
# the activation function will be relu
# the optimizer will be adam
# the loss function will be mse
# the ai will be trained using reinforcement learning
# the ai will be able to play against itself to train itself

# ai class
class ai_player(nn.Module):
    def __init__(self):
        super(ai_player, self).__init__()
        self.conv1 = nn.Conv2d(5, 128, 3)
        self.conv2 = nn.Conv2d(128, 64, 3)
        self.conv3 = nn.Conv2d(64, 32, 3)
        self.conv4 = nn.Conv2d(32, 16, 3)
        self.fc1 = nn.Linear(16 * 3 * 3, 64)
        self.fc2 = nn.Linear(64, 64)
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = x.view(-1, 16 * 3 * 3)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    

# ai class
class agent:
    def __init__(self):
        self.ai = ai_player()
        self.optimizer = optim.Adam(self.ai.parameters(), lr=0.001)
        self.loss = nn.MSELoss()
        self.board = np.zeros((8, 8, 5))
        self.turn = 0
        self.color = 1
        self.last_move = ""
        self.movement = []
    
    def move(self, move):
        if self.valid_move(move):
            self.board = self.make_move(move)
            self.turn += 1
            self.movement.append(move)
            return 1
        else:
            return -1


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
def print_board(board, last_move, turn, color: int):
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
        >>> print_board(board, last_move, turn, color = 1)
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
        delete_last_lines(17)
    if len(last_move) > 0:
        print("Last move: ", color, ' ', last_move)
    
    print()
    if color == 1:
        colorWo = "White"
    elif color == 2:
        colorWo = "Black"
    print('move from: ', colorWo)
    
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

# overwrite the board with the new board in the terminal
def delete_last_lines(n=1):
    """
    Deletes the last 'n' lines from the console output.

    Parameters:
    - n (int): The number of lines to delete. Default is 1.

    Returns:
    None
    """
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE, end='')

