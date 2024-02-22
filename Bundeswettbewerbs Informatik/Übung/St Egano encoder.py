from PIL import Image, ImageDraw
import numpy as np
import math
import random
import time
import os
import sys

def encode_image(image: Image, message: str):
    # message to ascii decimal
    message = [ord(c) for c in message]
    # r = ascii, g = nach rechts, b = nach unten
    # wenn g und b = 0, dann ist das ende des textes erreicht
    # durch g und b wird die position des nächsten buchstaben bestimmt
    # wenn g über den rand geht dann geht es auf der linken seite weiter
    # wenn b über den rand geht dann geht es auf der oberen seite weiter
    # Bild in numpy array umwandeln
    img = np.array(image)
    # Text einfügen
    curserG = 0
    curserB = 0
    g = random.randint(1, 255)
    b = random.randint(1, 255)
    altertPositions = [(curserG, curserB)]
    img[curserB, curserG, 1] = g
    img[curserB, curserG, 2] = b
    img[curserB, curserG, 0] = message[0]
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    draw.point((curserG, curserB), fill=(message[0], g, b))
    img = np.array(img)
    print(message[0])
    for i in range(1,len(message)):
        
        
        while g + curserG >= img.shape[1]:
            if g + curserG > img.shape[1] - 1:
                g = g - (img.shape[1] - curserG)
                curserG = 0
        
        while b + curserB >= img.shape[0]:
            if b + curserB > img.shape[0] - 1:
                b = b - (img.shape[0] - curserB)
                curserB = 0
        
        curserG += g
        curserB += b
        while (curserG, curserB) in altertPositions:
            b = random.randint(1, 255)
            g = random.randint(1, 255)
        
        altertPositions.append((curserG, curserB))
        
        img[curserB, curserG, 2] = g
        img[curserB, curserG, 1] = b
        if i % 100 >= 0:
            print(f"{i}/{len(message)}")
        
        img[curserB, curserG, 0] = message[i]
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        draw.point((curserG, curserB), fill=(message[i], g, b))
        img = np.array(img)
    img[curserB, curserG, 1] = 0
    img[curserB, curserG, 2] = 0
    img[curserB, curserG, 0] = message[i]
    # Bild speichern
    return Image.fromarray(img)

img: Image = encode_image(Image.open(sys.argv[1]), sys.argv[2])
img.save(sys.argv[3])