import numpy as np
from PIL import Image
import os
import time
import sys

removeLine = '\033[F'
moveUp = '\033[A'
moveDown = '\033[B'
clearScreen = '\033[2J'

def get_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error: {e}")
        return None

def resize_image(image, new_width):
    width_percent = (new_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))
    resized_image = image.resize((new_width, new_height), Image.NEAREST)
    return resized_image

# colors that i can use
# background colors for the most common color in an area of the image
# foreground colors for the second common color in an area of the image
colors = {
    0: Fore.BLACK,
    1: Fore.RED,
    2: Fore.GREEN,
    3: Fore.YELLOW,
    4: Fore.BLUE,
    5: Fore.MAGENTA,
    6: Fore.CYAN,
    7: Fore.WHITE,
    8: Back.BLACK,
    9: Back.RED,
    10: Back.GREEN,
    11: Back.YELLOW,
    12: Back.BLUE,
    13: Back.MAGENTA,
    14: Back.CYAN,
    15: Back.WHITE,
}

# symbols to represent the second common color in an area of the image
symbols = {
    0: ' ',
    1: '.',
    2: '-',
    3: '+',
    4: '*',
    5: 'x',
    6: '%',
    7: '#',
}

def most_common_color_of_area(image, x, y, width, height):
    colors = image.crop((x, y, x + width, y + height)).getcolors(width * height)
    return max(colors, key=lambda x: x[0])[1]

def second_common_color_of_area(image, x, y, width, height):
    colors = image.crop((x, y, x + width, y + height)).getcolors(width * height)
    colors = sorted(colors, key=lambda x: x[0], reverse=True)
    if len(colors) > 1:
        return colors[1][1]
    return colors[0][1]

def get_ratio_of_color(image, most_common_color, second_common_color, x, y, width, height):
    colors = image.crop((x, y, x + width, y + height)).getcolors(width * height)
    most_common_color_count = 0
    second_common_color_count = 0
    for color in colors:
        if color[1] == most_common_color:
            most_common_color_count += color[0]
        elif color[1] == second_common_color:
            second_common_color_count += color[0]
    return most_common_color_count / (most_common_color_count + second_common_color_count)