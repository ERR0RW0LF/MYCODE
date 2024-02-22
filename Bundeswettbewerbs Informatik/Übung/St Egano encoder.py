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
    for i in range(len(message)):
        img[curserB, curserG, 0] = message[i]
        if i < len(message) - 1:
            while g + curserG >= img.shape[1]:
                if g + curserG > img.shape[1] - 1:
                    g = g - (img.shape[1] - curserG)
                    curserG = 0
            
            while b + curserB >= img.shape[0]:
                if b + curserB > img.shape[0] - 1:
                    b = b - (img.shape[0] - curserB)
                    curserB = 0
            img[curserB, curserG, 1] = random.randint(0, 255)
            img[curserB, curserG, 2] = random.randint(0, 255)
            curserG += img[curserB, curserG, 1]
            curserB += img[curserB, curserG, 2]
            
    img[curserB, curserG, 1] = 0
    img[curserB, curserG, 2] = 0
    # Bild speichern
    return Image.fromarray(img)

encode_image(Image.open(sys.argv[1]), sys.argv[2]).save(sys.argv[3])