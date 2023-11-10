import turtle

def draw_fibonacci_spiral(n, m):
    a, b = 0, 1
    turtle.forward(b * m)
    turtle.backward(b * m)
    turtle.right(90)
    turtle.forward(b * m)

    for i in range(n):
        a, b = b, a + b
        turtle.backward(b * m)
        turtle.right(90)
        turtle.forward(b * m)

turtle.speed(1)
draw_fibonacci_spiral(20, 5)
turtle.done()
