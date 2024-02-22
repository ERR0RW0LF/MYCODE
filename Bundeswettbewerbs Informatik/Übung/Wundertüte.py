from shutil import SpecialFileError
import numpy as np
import sys
import os
import pandas as pd

# txt file path
file_path = sys.argv[1]

file = open(file_path, 'r')

wundertuetenAnzahl = int(file.readline())
spielsortenAnzahl = int(file.readline())
print('Wundertueten: ', wundertuetenAnzahl)
print()
print('Spielsorten: ', spielsortenAnzahl)

# spielsorten anzahl
spielsorten = []
for i in range(spielsortenAnzahl):
    spielsorten.append(int(file.readline()))

print()
print('Spielsorten: ', spielsorten)
print()

# gleich mäßig verteilen dann unterscheiden sich die Gesamtzahlen der Spiele zwischenje zwei Tüten um höchstens eins. Ebenso gilt auchfür jede Spielesorte, dass sich ihre Anzahlen zwischenje zwei Tüten um höchstens eins unterscheiden

# wundertueten erstellen
wundertueten = {}

for i in range(wundertuetenAnzahl):
    wundertueten[i] = []

# spiele gleichmäßig verteilen
for i in spielsorten:
    for j in range(wundertuetenAnzahl):
        wundertueten[j].append(i)
    
    # wundertueten nach wenigsten spielen sortieren erst wennig dann mehr
    wundertueten = dict(sorted(wundertueten.items(), key=lambda item: len(item[1])))

print(wundertueten)