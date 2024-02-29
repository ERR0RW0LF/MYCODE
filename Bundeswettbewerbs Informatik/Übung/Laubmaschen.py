import numpy as np
import matplotlib.pyplot as plt
import random

# Schulhof als 2D-Array 5*5 auf allen Planquadrat sind am Anfang 100 Blätter
schulhof = np.full((5, 5), 100)
print(schulhof)

# q: how can i display the 2D array as a grid so that i can see the 5*5 grid. leaves are displayed by a color gradient from green to white
plt.imshow(schulhof, cmap='Greens', interpolation='nearest')
input()