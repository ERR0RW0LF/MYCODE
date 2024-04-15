from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(RED, opacity=0.5)
        self.play(Create(circle))
        self.wait(1)