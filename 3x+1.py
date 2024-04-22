import pprint
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import random
import pprint

from sympy import true

class CollatzConjecture():
    def __init__(self, n):
        self.n = n
        b = n
        self.sequence = {b: [n]}
        while n != 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            self.sequence[b].append(n)
    
    def __str__(self):
        return str(self.sequence)
    
    def random(self, repetitions=1):
        self.sequence = {}
        for _ in range(repetitions):
            n = random.randint(1, 1000)
            if n in self.sequence:
                print(f"Already calculated for {n}")
            else:
                b = n
                self.sequence[b] = [n]
                while n != 1:
                    if n % 2 == 0:
                        n = n // 2
                    else:
                        n = 3 * n + 1
                    self.sequence[b].append(n)
    
    def inorder(self, repetitions=1):
        self.sequence = {}
        for n in range(1, repetitions+1):
            b = n
            
            if b == 1:
                primeN = False
            elif b > 1:
                for i in range(2, b):
                    if (b % i) == 0:
                        primeN = False
                        break
                    else:
                        primeN = True
            
            
            self.sequence[b] = [primeN, [n]]
            print(self.sequence[b][1])
            while n != 1:
                if n % 2 == 0:
                    n = n // 2
                else:
                    n = 3 * n + 1
                self.sequence[b][1].append(n)

    def plot(self):
        for key in self.sequence:
            if self.sequence[key][0] == True:
                plt.plot(self.sequence[key][1], color='red')
            else:
                plt.plot(self.sequence[key][1], color='blue')
            
        pprint.pprint(self.sequence)
        plt.grid(True)
        plt.show()

c = CollatzConjecture(27)
c.random(10)
pprint.pprint(c.inorder(1000))

c.plot()