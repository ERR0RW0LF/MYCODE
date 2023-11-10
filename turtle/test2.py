from turtle import *

r = 0
g = 0
b = 0
colormode(255)
width(3)
speed(0)
for r in range(0, 250):
    for g in range(0, 250):
        for b in range(0, 250):
            b += 5
            pencolor((r, g, b))
            forward(1)
            left(1)
        b = 0
        g += 5
        pencolor((r, g, b))
        forward(1)
        left(1)
    b = 0
    g = 0
    r += 5
    pencolor((r, g, b))
    forward(1)
    left(1)


