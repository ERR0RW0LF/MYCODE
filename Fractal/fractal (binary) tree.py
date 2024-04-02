import turtle
import time
from PIL import Image, ImageDraw, ImageFont
import math


def generate_fractal_tree(iterations: int = 10):
    tree = '0'
    tree_new = ''
    for t in range(iterations):
        for i in range(len(tree)):
            if tree[i] == '0':
                tree_new = tree_new + '1[0]0'
            elif tree[i] == '1':
                tree_new = tree_new + '11'
            elif tree[i] == '[':
                tree_new = tree_new + '['
            elif tree[i] == ']':
                tree_new = tree_new + ']'
        
        #print(t , '. ' , tree_new)
        tree = tree_new
        tree_new = ''
    
    return tree

def draw_fractal_tree(tree: str):
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.bgcolor('black')
    turtle.color('green')
    
    turtle.speed(0)
    turtle.left(180)
    turtle.penup()
    turtle.goto(700, 450)
    turtle.pendown()
    
    print('Drawing tree...')
    
    time.sleep(1)
    
    d = 0
    frame = 0
    
    for d in range(len(tree)):
        if tree[d] == '0':
            turtle.color('red')
            turtle.forward(1)
            turtle.color('green')
        elif tree[d] == '1':
            turtle.forward(1)
        elif tree[d] == '[':
            turtle.left(45)
        elif tree[d] == ']':
            turtle.right(45)
        
        if turtle.xcor() > 900 - frame:
            frame -= 5
            turtle.pensize(5)
            turtle.color('cyan')
            turtle.forward(1)
            turtle.penup()
            turtle.goto(-900 + frame + 5, turtle.ycor())
            turtle.pendown()
            turtle.speed(0)
            turtle.pensize(1)
            turtle.color('green')
        if turtle.xcor() < -900 + frame:
            frame -= 5
            turtle.pensize(5)
            turtle.color('cyan')
            turtle.forward(1)
            turtle.penup()
            turtle.goto(900 - frame - 5, turtle.ycor())
            turtle.pendown()
            turtle.speed(0)
            turtle.pensize(1)
            turtle.color('green')
        if turtle.ycor() > 450 - frame:
            frame -= 5
            turtle.pensize(2)
            turtle.color('cyan')
            turtle.forward(1)
            turtle.penup()
            turtle.goto(turtle.xcor(), -450 + frame + 5)
            turtle.pendown()
            turtle.speed(0)
            turtle.pensize(1)
            turtle.color('green')
        if turtle.ycor() < -450 + frame:
            frame -= 5
            turtle.pensize(2)
            turtle.color('cyan')
            turtle.forward(1)
            turtle.penup()
            turtle.goto(turtle.xcor(), 450 - frame - 5)
            turtle.pendown()
            turtle.speed(0)
            turtle.pensize(1)
            turtle.color('green')
        
        if frame < 100:
            frame = 0
        
        time.sleep(0.0001)
    
    print(len(str(tree)))
    
    print('Done!')
    
    turtle.done()

def draw_picture(tree:str):
    d = 1

    while tree[d] == '1':
        d += 1
    
    print(d)
    
    img = Image.new('RGB', (d*10, d*10), color = 'black')
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.load_default()
    
    posX = d*2
    posY = d/4
    ang = 0
    
    rotationBox = 10
    
    for i in range(len(tree)):
        if tree[i] == '0':
            newPos = calculate_new_position(posX, posY, ang, 4)
            newPosX = newPos[0]
            newPosY = newPos[1]
            img_draw.line((posX, posY, newPosX, newPosY), fill='red', width=5)
            posX = newPosX
            posY = newPosY
        elif tree[i] == '1':
            newPos = calculate_new_position(posX, posY, ang, 4)
            newPosX = newPos[0]
            newPosY = newPos[1]
            img_draw.line((posX, posY, newPosX, newPosY), fill='green', width=5)
            posX = newPosX
            posY = newPosY
        elif tree[i] == '[':
            ang += 45
            img_draw.rectangle((posX-rotationBox, posY-rotationBox, posX+rotationBox, posY+rotationBox), fill='blue')
        elif tree[i] == ']':
            ang -= 45
            img_draw.rectangle((posX-rotationBox, posY-rotationBox, posX+rotationBox, posY+rotationBox), fill='yellow')
        
        print()
        print(i)
        print(newPos)
        print(newPosX, newPosY)
        print(posX, posY)
    
    img.save('tree3.png')


def calculate_new_position(start_x, start_y, direction, length):
    # Convert direction from degrees to radians
    direction_rad = math.radians(direction)

    # Calculate new position
    end_x = start_x + length * math.cos(direction_rad)
    end_y = start_y + length * math.sin(direction_rad)

    return end_x, end_y


if __name__ == '__main__':
    tree = generate_fractal_tree(11)
    #draw_fractal_tree(tree)
    draw_picture(tree)
