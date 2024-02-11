from calendar import c
from hmac import new
import imp
from math import e, log
import random
from re import T
from matplotlib.pyplot import pie
import numpy as np
import logging
import time
from pyparsing import col
from requests import get
#import keras
import tensorflow as tf
from tensorflow import keras
import os
import sys
import mcts

# load the models if they are available and if not create them and save them
def test_gpu():
    """
    Tests if a GPU is available for use with TensorFlow.

    Returns:
    - None

    Prints a message indicating whether a GPU is available for use with TensorFlow.
    """
    if tf.test.is_gpu_available():
        print("Using GPU")
    else:
        print("Using CPU")

# create_model() creates a model for the white and black player and returns them input (8, 8, 5) output which piece to move and where to move it in the format [x, y, x, y] (0-7) (0-7) (0-7) (0-7)
def create_model():
    """
    Creates a model for the white and black player and returns them.

    Returns:
    - model: The model for the white and black player.

    The model is a convolutional neural network with 5 layers.
    The input shape is (8, 8, 5) and the output shape is (8, 8, 8, 8).
    """
    model = keras.Sequential([
        keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu', padding='same', input_shape=(8, 8, 5)),
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
        keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu', padding='same', input_shape=(8, 8, 5)),
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        # output layer
        keras.layers.Dense(8, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# create_model_evaluation() creates a model for the evaluation of the current state of the game and returns it input (8, 8, 5) output the evaluation of the current state of the game
def create_model_evaluation():
    """
    Creates a model for the evaluation of the current state of the game and returns it.

    Returns:
    - model: The model for the evaluation of the current state of the game.

    The model is a convolutional neural network with 5 layers.
    The input shape is (8, 8, 5) and the output shape is (1, 1, 1).
    """
    model = keras.Sequential([
        keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu', padding='same', input_shape=(8, 8, 5)),
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
        keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu', padding='same', input_shape=(8, 8, 5)),
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        # output layer
        keras.layers.Dense(1, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


# training loop for all models using reinforcement learning
def train_model(model_white, model_black, model_evaluation, games=1000):
    """
    Trains the models for the white and black player and the evaluation model using reinforcement learning.

    Args:
    - model_white: The model for the white player.
    - model_black: The model for the black player.
    - model_evaluation: The evaluation model.
    - games: The number of games to play for training. Defaults to 1000.

    Returns:
    - model_white: The trained model for the white player.
    - model_black: The trained model for the black player.
    - model_evaluation: The trained evaluation model.

    The models are trained using reinforcement learning.
    The models are trained to play chess using the Monte Carlo Tree Search algorithm.
    """
    for i in range(games):
        board = np.zeros((8, 8, 5))
        turn = 0
        while True:
            valid_move = False
            while valid_move == False:
                if turn % 2 == 0:
                    move = mcts.mcts(board, model_white, model_evaluation)
                    # q: what does mcts do?
                    # a: mcts is the Monte Carlo Tree Search algorithm
                    # q: what is the Monte Carlo Tree Search algorithm?
                    # a: The Monte Carlo Tree Search algorithm is a heuristic search algorithm that uses random sampling to find the best move in a game.
                    # q: why do i get this error: TypeError: 'module' object is not callable?
                    # a: The error occurs when you try to call a module as a function. You should call the function inside the module instead.
                    # q: how do i fix the error?
                    # a: You should call the function inside the module instead of the module itself.
                else:
                    move = mcts.mcts(board, model_black, model_evaluation)
            moved = move_piece_ai(board, move[0], move[1], move[2], move[3])
            if moved[0].all() == board.all():
                continue
            board = moved[0]
            print_board(board, moved[2], turn, color = turn % 2 + 1)
            winner = get_winner(board)
            if winner != 0:
                # reward the models based on the winner
                if winner == 1:
                    rewardBlack = -1
                    rewardWhite = 1
                elif winner == 2:
                    rewardBlack = 1
                    rewardWhite = -1
                else:
                    rewardBlack = 0
                    rewardWhite = 0
                break
            turn += 1
        if i % 100 == 0:
            print("Game", i, "completed")
        model_black = keras.train_model(model_black, board, rewardBlack)
        model_white = keras.train_model(model_white, board, rewardWhite)
        model_evaluation = keras.train_model_evaluation(model_evaluation, board, rewardWhite)
    return model_white, model_black, model_evaluation

# initialize the models for white and black and an evaluation model
def initialize_models():
    """
    Initializes the models for white and black and an evaluation model.

    Returns:
    - model_white: The model for the white player.
    - model_black: The model for the black player.
    - model_evaluation: The evaluation model.

    If the models are available, they are loaded from the disk.
    If the models are not available, they are created and saved to the disk.
    """
    try:
        model_white = keras.models.load_model("model_white")
        model_black = keras.models.load_model("model_black")
        model_evaluation = keras.models.load_model("model_evaluation")
    except:
        model_white = create_model()
        model_black = create_model()
        model_evaluation = create_model_evaluation()
        model_white.save("model_white")
        model_black.save("model_black")
        model_evaluation.save("model_evaluation")
    return model_white, model_black, model_evaluation


# check_mate() checks if the game is over
def check_mate(board, color):
    """
    Checks if the game is over.

    Args:
    - board: The current state of the chessboard.
    - color: The color of the player to check for checkmate.

    Returns:
    - True if the game is over, False otherwise.

    The game is over if the player of the given color is in checkmate.
    """
    winner = 0
    if get_winner(board, color) == 0:
        return False
    else:
        return True
    return False

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
def knight_patern(board, x, y, color=0):
    """
    Generates a pattern for the possible moves of a knight on a chessboard.

    Parameters:
    - board: numpy array representing the chessboard
    - x: x-coordinate of the knight's position
    - y: y-coordinate of the knight's position
    - color: color of the knight (0 for neutral, 1 for white, 2 for black)

    Returns:
    - patern: numpy array representing the pattern of possible moves for the knight
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
def rook_patern(board, x, y, color=0):
    """
    Generates a pattern for a rook piece on a chessboard.

    Args:
        board (numpy.ndarray): The chessboard represented as a 3D numpy array.
        x (int): The x-coordinate of the rook's position on the board.
        y (int): The y-coordinate of the rook's position on the board.
        color (int, optional): The color of the rook. Defaults to 0.

    Returns:
        numpy.ndarray: A 2D numpy array representing the rook's pattern on the board.
            - 0: Empty square
            - 1: Valid move
            - 2: Capture move
            - 3: Rook's current position
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
import numpy as np

def queen_patern(board, x, y, color=0):
    """
    Generates a pattern for the queen piece on a chessboard.

    Parameters:
    - board (numpy.ndarray): The chessboard represented as a 3D numpy array.
    - x (int): The x-coordinate of the queen's position on the board.
    - y (int): The y-coordinate of the queen's position on the board.
    - color (int): The color of the queen (0 for neutral, 1 for white, 2 for black).

    Returns:
    - patern (numpy.ndarray): The pattern generated for the queen piece on the chessboard.

    The pattern is represented as a 2D numpy array with the same shape as the chessboard.
    Each element in the pattern represents the possible moves for the queen from its current position.
    - 0: The queen cannot move to this position.
    - 1: The queen can move to this position.
    - 2: The queen can capture an enemy piece at this position.
    - 3: The queen's current position.

    Note: The pattern is generated based on the current state of the chessboard and the queen's color.
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
def king_patern(board, x, y, color=0, moved=0):
    """
    Generates a pattern for the possible moves of a king on a chessboard.

    Args:
        board (numpy.ndarray): The chessboard represented as a 3D numpy array.
        x (int): The x-coordinate of the king's position.
        y (int): The y-coordinate of the king's position.
        color (int, optional): The color of the king. 0 for no color, 1 for white, 2 for black. Defaults to 0.
        moved (int, optional): Indicates whether the king has moved before. 0 for not moved, 1 for moved. Defaults to 0.

    Returns:
        numpy.ndarray: A 2D numpy array representing the pattern of possible moves for the king.
            - 0: The king's current position.
            - 1: A valid move for the king.
            - 2: A valid move that captures an enemy piece.
            - 3: King's current position.
            - 4: Special move (castling).

    """
    
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
def pawn_patern(board, x, y, color=0):
    """
    Generates a pattern for a pawn's possible moves on a chessboard.

    Args:
        board (numpy.ndarray): The chessboard represented as a 3D numpy array.
        x (int): The x-coordinate of the pawn's position on the chessboard.
        y (int): The y-coordinate of the pawn's position on the chessboard.
        color (int, optional): The color of the pawn. 0 for neutral, 1 for white, 2 for black. Defaults to 0.

    Returns:
        numpy.ndarray: A 2D numpy array representing the pattern of possible moves for the pawn.

    Note:
        - The pattern array is initialized with zeros.
        - The pattern array is modified to indicate possible moves for the pawn.
        - The pattern array uses the following values:
            - 0: Empty square
            - 1: Valid move
            - 2: Capture move
            - 3: Current position of the pawn
            - 5: Special move (e.g., double pawn move)

    """
    
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
    """
    Promotes a pawn on the chess board.

    Args:
        board (numpy.ndarray): The chess board.
        x (int): The x-coordinate of the pawn.
        y (int): The y-coordinate of the pawn.
        color (int): The color of the pawn (1 for white, 2 for black).
        piece (int): The piece to promote the pawn to.

    Returns:
        numpy.ndarray: The updated chess board.
    """
    if color == 1:
        if x == 0:
            board[x, y, 1] = piece
    elif color == 2:
        if x == 7:
            board[x, y, 1] = piece
    return board

# promote to random piece
def promote_pawn_random(board, x, y, color):
    """
    Promotes a pawn on the chess board randomly.

    Args:
        board (numpy.ndarray): The chess board represented as a 3D numpy array.
        x (int): The x-coordinate of the pawn.
        y (int): The y-coordinate of the pawn.
        color (int): The color of the pawn (1 for white, 2 for black).

    Returns:
        numpy.ndarray: The updated chess board after promoting the pawn.
    """
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
    """
    Prints the given pattern.

    Args:
        patern (list or any): The pattern to be printed. It can be a list or any other type.

    Returns:
        None
    """
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
    """
    Calculates the number of possible moves for a given piece on the chessboard.

    Parameters:
    - board: numpy array representing the chessboard
    - x: x-coordinate of the piece
    - y: y-coordinate of the piece

    Returns:
    - count: number of possible moves for the piece

    Note:
    - The board is a 3-dimensional numpy array where the first dimension represents the x-coordinate,
      the second dimension represents the y-coordinate, and the third dimension represents the piece type,
      player, and additional information.
    - The piece type is represented by the value in the third dimension at index 0.
    - The player is represented by the value in the third dimension at index 1.
    - Additional information about the piece (e.g., whether it has moved) is represented by the value in the third dimension at index 2.
    - The count of possible moves is calculated based on the piece type and its current position on the board.

    """
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
    """
    Returns the pattern for the piece at the given position on the board.

    Parameters:
    - board: The chess board.
    - x: The x-coordinate of the piece.
    - y: The y-coordinate of the piece.

    Returns:
    - The pattern for the piece at the given position.

    """
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
    """
    Moves a piece on the chess board.

    Args:
        board (numpy.ndarray): The chess board represented as a 3D numpy array.
        x (int): The x-coordinate of the piece to be moved.
        y (int): The y-coordinate of the piece to be moved.
        move (int): The number of moves to be made.
        turn (int): The current turn number.
        moves (list): The list of previous moves.

    Returns:
        tuple: A tuple containing the updated board, the updated list of moves, and the last move made.

    Raises:
        None

    """
    
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

import random

def random_piece(board, turn):
    """
    Selects a random movable piece from the given chess board for the specified turn.

    Parameters:
    - board (numpy.ndarray): The chess board represented as a 3D numpy array.
    - turn (int): The current turn number.

    Returns:
    - tuple or None: A tuple representing the coordinates of the randomly selected movable piece,
      or None if there are no movable pieces.

    """
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
    """
    Returns a random move for the given board and position.

    Parameters:
    board (list): The chess board.
    x (int): The x-coordinate of the position.
    y (int): The y-coordinate of the position.

    Returns:
    int: A random move index.

    """
    return random.randint(0, get_possible_moves(board, x, y) - 1)

# determine the winner of the game
def get_winner(board):
    """
    Determines the winner of a chess game based on the current state of the board.

    Args:
        board (numpy.ndarray): The chess board represented as a 3D numpy array.

    Returns:
        int: The winner of the game. Possible return values:
            - 0: The game is still ongoing.
            - 1: White player wins.
            - 2: Black player wins.
            - 3: The game is a draw.
    """
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
    """
    Converts the winner value to a readable string representation.

    Args:
        winner (int): The winner value. Possible values are:
            - 0: No winner
            - 1: White wins
            - 2: Black wins
            - 3: Draw

    Returns:
        str: The readable string representation of the winner.

    """
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
    """
    Perform a round of the chess game.

    Args:
        board (numpy.ndarray): The current state of the chess board.
        turn (int): The current turn number.
        moves (str): The string representation of the previous moves.

    Returns:
        tuple: A tuple containing the updated board, turn number, moves, and the last move made.

    """
    # q: how can i check if two numpy arrays with 3 dimensions are equal?
    # a: np.array_equal(array1, array2)
    
    piece = random_piece(board, turn)
    if piece == None:
        return board, turn, moves, ""
    move = random_move(board, piece[0], piece[1])
    move_out = move_piece(board, piece[0], piece[1], move, turn, moves)
    board = np.array(move_out[0])
    moves = move_out[1]
    last_move = move_out[2]
    return board, turn + 1, moves, last_move

# main function
def main(board, turn: int, moves):
    """
    Runs the main game loop for the chess game.

    Args:
        board (list): The current state of the chess board.
        turn (int): The current turn number.
        moves (list): The list of moves made so far.

    Returns:
        tuple: A tuple containing the updated board, turn, moves, and the winner of the game.
    """
    #print('\n' * 17)
    r = 0
    winner = get_winner(board)
    color = 0
    while winner == 0:
        if turn % 2 + 1 == 1:
            color = 1
        else:
            color = 2
        old_turn = turn
        board, turn, moves, last_move = round(board, turn, moves)
        if old_turn == turn or last_move == "":
            r += 1
            print_board(board, str(r), turn, color=color)
            
        else:
            r = 0
            print_board(board, last_move, turn, color=color)
        
        time.sleep(0.00001)
        winner = get_winner(board)
        
    print("Winner: ", readable_winner(get_winner(board)))
    #print("Moves: ")
    print()
    #for i in moves:
    #    print(i)
    print(turn)
    print('\n' * 17)
    winner = get_winner(board)
    return board, turn, moves, winner

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

# check if a move is valid
def is_valid_move(board, x, y, newX, newY):
    patern = get_patern(board, x, y)
    if patern[newX, newY] == 1 or patern[newX, newY] == 2 or patern[newX, newY] == 4 or patern[newX, newY] == 5:
        return True
    elif patern[newX, newY] == 3:
        return False
    else:
        return False


# move a piece on the board for ai
def move_piece_ai(board, x, y, newX, newY, turn):
    """
    Moves a piece on the chess board.

    Args:
        board (numpy.ndarray): The chess board represented as a 3D numpy array.
        x (int): The x-coordinate of the piece to be moved.
        y (int): The y-coordinate of the piece to be moved.
        newX (int): The x-coordinate of the new position.
        newY (int): The y-coordinate of the new position.
        turn (int): The current turn number.

    Returns:
        tuple: A tuple containing the updated board, the updated list of moves, and the last move made.

    """
    pattern = get_patern(board, x, y)
    last_move = ""
    if is_valid_move(board, x, y, newX, newY) == False:
        return board, [], last_move
    if pattern[newX, newY] == 5:
        board[newX, newY] = board[x, y]
        board[newX, newY, 3] = 1
        board[newX, newY, 4] = turn
        if pattern[newX, newY] == 5 and board[x, y, 0] == 1 and x == 6:
            board[newX + 1, newY] = board[x, y]
            board[newX + 1, newY, 3] = 2
            board[newX + 1, newY, 4] = turn
            board[x, y] = [0, 0, 0, 0, 0]
            return board, [], last_move
        elif pattern[newX, newY] == 5 and board[x, y, 0] == 2 and x == 6:
            board[newX - 1, newY] = board[x, y]
            board[newX - 1, newY, 3] = 2
            board[newX - 1, newY, 4] = turn
            board[x, y] = [0, 0, 0, 0, 0]
            return board, [], last_move
    elif pattern[newX, newY] == 4:
        board[newX, newY] = board[x, y]
        board[newX, newY, 2] += 1
        board[newX, newY, 4] = turn
        board[x, y] = [0, 0, 0, 0, 0]
        if newX == 7 and newY == y + 2:
            board[7, 5] = board[7, 7]
            board[7, 5, 2] += 1
            board[7, 5, 4] = turn
            board[7, 7] = [0, 0, 0, 0, 0]
            return board, [], last_move
        elif newX == 7 and newY == y - 2:
            board[7, 3] = board[7, 0]
            board[7, 3, 2] += 1
            board[7, 3, 4] = turn
            board[7, 0] = [0, 0, 0, 0, 0]
            return board, [], last_move
    elif pattern[newX, newY] == 2:
        if board[newX, newY, 3] == 2:
            if board[newX, newY, 0] == 1:
                board[newX, newY] = board[x, y]
                board[newX, newY, 3] = 1
                board[newX, newY, 4] = turn
                board[newX - 1, newY] = [0, 0, 0, 0, 0]
                board[x, y] = [0, 0, 0, 0, 0]
                return board, [], last_move
            elif board[newX, newY, 0] == 2:
                board[newX, newY] = board[x, y]
                board[newX, newY, 3] = 1
                board[newX, newY, 4] = turn
                board[newX + 1, newY] = [0, 0, 0, 0, 0]
                board[x, y] = [0, 0, 0, 0, 0]
                return board, [], last_move
        else:
            board[newX, newY] = board[x, y]
            board[newX, newY, 3] = 1
            board[newX, newY, 4] = turn
            board[x, y] = [0, 0, 0, 0, 0]
            if board[newX, newY, 1] == 1:
                board = promote_pawn_random(board, newX, newY, board[newX, newY, 0])
            return board, [], last_move
        board[newX, newY] = board[x, y]
        board[newX, newY, 2] += 1
        board[newX, newY, 4] = turn
        if board[newX, newY, 1] == 1:
            board = promote_pawn_random(board, newX, newY, board[newX, newY, 0])
        board[x, y] = [0, 0, 0, 0, 0]
    board[newX, newY] = board[x, y]
    board[newX, newY, 2] += 1
    board[newX, newY, 4] = turn
    if board[newX, newY, 1] == 1:
        board = promote_pawn_random(board, newX, newY, board[newX, newY, 0])
    board[x, y] = [0, 0, 0, 0, 0]
    return board, [], last_move


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

# If the current module is being executed as the main script
if __name__ == "__main__":
    tf.config.list_physical_devices('GPU')
    test_gpu()
    model_white, model_black, model_evaluation = initialize_models()
    if sys.argv[1] == "t":
        print("Training")
        model_white, model_black, model_evaluation = train_model(model_white, model_black, model_evaluation)
    else:
        print("Not training")
    exit()
    # Set up the logging configuration to display warning messages and above
    logging.basicConfig(level=logging.WARNING)
    
    # Log that the script has started
    logging.info('Started')
    
    # Log that the required modules have been imported
    logging.info('Imported modules')
    
    # Log that the game is starting
    logging.info('Starting the game')
    
    # Initialize the game variables
    turn = 0
    board = board_base
    winnes = []
    turns = []
    
    random.seed(random.random())
    
    # Play the game 1000 times
    for i in range(50):
        # Call the main function to play a single game and get the updated board, turn, movement, and winner
        board, turn, movement, winner = main(board, turn, [])
        
        # Append the winner and turn to the respective lists
        winnes.append(winner)
        turns.append(turn)
        
        # Reset the board and turn for the next game
        board_base = board_base
        board = board_base
        turn = 0
        
        # Print the game number
        print("Game: ", i + 1)
        random.seed(random.random())
    
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
    
    # Print the statistics of the games
    print("White wins: ", winnesW)
    print("Black wins: ", winnesB)
    print("Draws: ", winnesD)
    print("Average turns: ", sum(turns) / len(turns))
    
    # Print the percentage of wins for each player
    print("White wins: ", winnesW / len(winnes) * 100, "%")
    print("Black wins: ", winnesB / len(winnes) * 100, "%")
    print("Draws: ", winnesD / len(winnes) * 100, "%")
    time.sleep(1)
    print()
    print('---------------------------------')
    print()
    time.sleep(5)
    board_base = board_base
    
    # Play the game 1000 times
    for i in range(50):
        # Call the main function to play a single game and get the updated board, turn, movement, and winner
        board, turn, movement, winner = main(board, turn, [])
        
        # Append the winner and turn to the respective lists
        winnes.append(winner)
        turns.append(turn)
        
        # Reset the board and turn for the next game
        board_base = board_base
        board = board_base
        turn = 0
        
        # Print the game number
        print("Game: ", i + 1)
        random.seed(random.random())
    
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
    
    # Print the statistics of the games
    print('Games: ', len(winnes))
    print("White wins: ", winnesW)
    print("Black wins: ", winnesB)
    print("Draws: ", winnesD)
    print("Average turns: ", sum(turns) / len(turns))
    
    # Print the percentage of wins for each player
    print("White wins: ", winnesW / len(winnes) * 100, "%")
    print("Black wins: ", winnesB / len(winnes) * 100, "%")
    print("Draws: ", winnesD / len(winnes) * 100, "%")
    
    # Print the Unicode representation of the white and black king pieces
    print('\u2654')  # Black king
    print('\u265A')  # White king
