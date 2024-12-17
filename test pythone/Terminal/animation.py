import pprint
import time
import numpy as np
from colorama import Fore, Back, Style

removeLine = '\033[F'
moveUp = '\033[A'
moveDown = '\033[B'
clearScreen = '\033[2J'

symbols = {
    0: '  ',
    1: '▁▁',
    2: '▂▂',
    3: '▃▃',
    4: '▄▄',
    5: '▅▅',
    6: '▆▆',
    7: '▇▇',
    8: '██',
}

class Animation:
    def __init__(self, num_frames:int, sizeX:int, sizeY:int, delay:float):
        self.X = sizeX
        self.Y = sizeY
        self.num_frames = num_frames
        self.animation = np.zeros((num_frames,sizeX, sizeY), dtype=int)
        self.delay = delay
        self.frame = 0
        pprint.pprint(self.animation)
    
    def set_animation(self, animation:np.ndarray):
        self.animation = animation
    
    def set_symbol_at(self, x, y, frame, symbol):
        self.animation[frame][x][y] = symbol
    
    def set_frame(self, frame):
        self.frame = frame
    
    def set_symbol(self, x, y, symbol):
        self.animation[self.frame][x][y] = symbol
    
    def move(self, x, y, dx, dy):
        symbol = self.animation[self.frame][x][y]
        self.animation[self.frame][x][y] = 0
        self.animation[self.frame][x+dx][y+dy] = symbol
    
    def renderFrame(self, StyleRender=Fore.BLUE + Back.GREEN):
        printStyle = StyleRender
        frameRender = printStyle
        for y in range(self.Y):
            frameRender += printStyle
            for x in range(self.X):
                frameRender += symbols[self.animation[self.frame][x][y]]
            frameRender += Style.RESET_ALL + '\n'
        frameRender += Style.RESET_ALL
        return frameRender
    
    def play(self, StyleRender=Fore.BLUE + Back.GREEN):
        print(clearScreen)
        print(moveUp*self.Y)
        move(0,0)
        #print(moveDown*self.Y)
        print(removeLine*self.Y)
        print(Style.RESET_ALL)
        for frame in range(self.num_frames):
            self.set_frame(frame)
            print(self.renderFrame(StyleRender)+Style.RESET_ALL)
            time.sleep(self.delay)
            if frame < self.num_frames-1:
                move(0,0)
                #print(moveDown*self.Y)
                print(removeLine*self.Y)
                print(Style.RESET_ALL)
            else:
                print(clearScreen)
                print(moveUp*self.Y)
                print(Style.RESET_ALL)

def move (y, x):
    print("\033[%d;%dH" % (y, x))

def rotateArray(array:np.ndarray):
    rotated = np.zeros((array.shape[0],array.shape[2],array.shape[1]), dtype=int)
    
    for frame in range(array.shape[0]):
        for x in range(array.shape[1]):
            for y in range(array.shape[2]):
                rotated[frame][y][x] = array[frame][x][y]
    
    return rotated


compleatAnimation = np.array([
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,0],
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,0,0,1],
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [0,0,0,0,0,0,0,1,2],
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,0,1,2,3],
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,0,1,2,3,4],
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,0,1,2,3,4,5],
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,0,1,2,3,4,5,6],
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,0,1,2,3,4,5,6,7],
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [0,1,2,3,4,5,6,7,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [1,2,3,4,5,6,7,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    [
        [2,3,4,5,6,7,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [3,4,5,6,7,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [4,5,6,7,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [5,6,7,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [6,7,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [7,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ], 
    [
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8],
        [8,8,8,8,8,8,8,8,8]
        ],
    ])


compleatAnimation = rotateArray(compleatAnimation)

framesN = compleatAnimation.shape[0]
symbolsX = compleatAnimation.shape[1]
symbolsY = compleatAnimation.shape[2]
animation = Animation(framesN, symbolsX, symbolsY, 0.1)
animation.set_animation(compleatAnimation)
animation.play(StyleRender=Fore.LIGHTRED_EX+Back.BLUE)
animation.play(StyleRender=Fore.BLUE+Back.LIGHTRED_EX)

print(Fore.GREEN + "Animation is compleated!" + Style.RESET_ALL)