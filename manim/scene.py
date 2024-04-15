from manim import *
import numpy as np
import random

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(RED, opacity=0.5)
        self.play(Create(circle))
        self.wait(1)


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency
        

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class SortingAlgorithm(Scene):
    def construct(self):
        random.seed(0)
        array = []
        for i in range(1, 11):
            array.insert(random.randint(0, len(array)), i)
        
        square1 = Square()
        
        
        