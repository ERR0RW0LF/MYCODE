# drag files into the terminal to use it as files to edit with this script

import sys
import os
import re
import shutil
from PIL import Image, ImageDraw2, ImageDraw
import numpy as np
from pprint import pprint

# get the files to edit
files = input("Enter the files to edit: ").split(" ")

# check if a file is valid by existing and being a png file
def is_valid_file(file):
    if not os.path.exists(file):
        print(f"File {file} does not exist.")
        return False
    if not file.endswith(".png"):
        print(f"File {file} is not a png file.")
        return False
    return True

def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def hex_from_color(color):
    rgb = color[:3]
    return f"#{''.join(f'{c:02x}' for c in rgb)}"

images = {}
for file in files:
    if is_valid_file(file):
        images[file] = Image.open(file).convert("RGBA")

# get a list of all the colors in an image
def get_colors(image):
    colors = set()
    for x in range(image.width):
        for y in range(image.height):
            colors.add(image.getpixel((x, y)))
    return colors

# get the colors of all the images
colors = []
for file in images:
    colors = get_colors(images[file])

# remove all colors that have an alpha value of 0
colors = [color for color in colors if color[3] != 0]


print("Colors:")
for color in colors:
    print(hex_from_color(color), color)

# create a new image with the colors to replace. the width is the number of colors and the height is 2.
# the top row is the original color and the bottom row is the new color
new_image = Image.new("RGBA", (len(colors), 2))
for i, color in enumerate(colors):
    new_image.putpixel((i, 0), color)
    new_image.putpixel((i, 1), color)

new_image.save("replacement_colors.png")
new_image.close()

# wait until the user has edited the replacement_colors.png file
input("Edit the replacement_colors.png file and press enter to continue.")

# open the edited replacement_colors.png file
replacement_colors_image = Image.open("replacement_colors.png").convert("RGBA")

# get the colors from the replacement_colors.png file
replacement_colors = {}
for x in range(replacement_colors_image.width):
    original_color = replacement_colors_image.getpixel((x, 0))
    new_color = replacement_colors_image.getpixel((x, 1))
    replacement_colors[original_color] = new_color

replaced_images = {}
# replace the colors in the images
for file in images:
    image: Image = images[file]
    for x in range(image.width):
        for y in range(image.height):
            color = image.getpixel((x, y))
            if color in replacement_colors:
                image.putpixel((x, y), replacement_colors[color])

    replaced_images[file] = image

# rename the original images to have _original at the end
for file in images:
    os.rename(file, file.replace(".png", "_original.png"))

# save the replaced images at the same location as the original images with the same name but with _edited at the end
for file in replaced_images:
    replaced_images[file].save(file)
