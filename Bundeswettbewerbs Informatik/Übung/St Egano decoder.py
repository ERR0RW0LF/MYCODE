from PIL import Image
import numpy as np
import os
import sys

# Aus bildern text auslesen und drucken
# r = ascii, g = nach rechts, b = nach unten
# wenn g und b = 0, dann ist das ende des textes erreicht
# durch g und b wird die position des nächsten buchstaben bestimmt
# wenn g über den rand geht dann geht es auf der linken seite weiter
# wenn b über den rand geht dann geht es auf der oberen seite weiter

# Bild laden
img = Image.open(sys.argv[1])

# Bild in numpy array umwandeln
img = np.array(img)

# Text auslesen
text = ""
asciiR = []
g = 0
b = 0

curserG = 0
curserB = 0

asciiR.append(img[curserB, curserG, 0])
text += chr(img[curserB, curserG, 0])

g = img[curserB, curserG, 1]
b = img[curserB, curserG, 2]

while True:
    
    while g + curserG >= img.shape[1]: 
        if g + curserG > img.shape[1] - 1:
            g = g - (img.shape[1] - curserG)
            curserG = 0
    
    while b + curserB >= img.shape[0]:
        if b + curserB > img.shape[0] - 1:
            b = b - (img.shape[0] - curserB)
            curserB = 0
    
    asciiR.append(img[curserB, curserG, 0])
    curserG += g
    curserB += b
    
    g = img[curserB, curserG, 1]
    b = img[curserB, curserG, 2]
    
    text += chr(img[curserB, curserG, 0])
    if g == 0 and b == 0:
        break

print()
print('-'*50)
print()
print(text)
print()
print('-'*50)
print()

if os.path.exists(f'{sys.argv[1]}.txt'):
    os.remove(f'{sys.argv[1]}.txt')
testfile = open(f'{sys.argv[1]}.txt', 'w')
testfile.write(text)
testfile.close()