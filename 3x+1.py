import pprint
import matplotlib.pyplot as plt
import numpy as np
import random
import pprint
from numba import cuda

cuda.select_device(0)

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
            inDict = False
            #skip if already calculated
            for key in self.sequence:
                if n in self.sequence[key][1]:
                    inDict = True
                    break
            
            if inDict:
                continue
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
                
                for key in self.sequence:
                    if n in self.sequence[key][1]:
                        inDict = True
                        break
                
                if inDict:
                    break
                
                self.sequence[b][1].append(n)

    def plot(self):
        for key in self.sequence:
            if self.sequence[key][0] == True:
                plt.plot(self.sequence[key][1], color='red')
            else:
                plt.plot(self.sequence[key][1], color='blue')
            
            print(key, self.sequence[key][0], self.sequence[key][1])
        
        plt.grid(True)
        plt.show()
    
    def getAllValuesAsList(self):
        allValues = []
        for key in self.sequence:
            allValues += self.sequence[key][1]
        
        return allValues

    def getAllNotExistentValuesAsList(self):
        allValues = self.getAllValuesAsList()
        allNotValues = []
        allValues.sort()
        allValues.reverse()
        maxValue = allValues.index(1)
        for i in range(maxValue):
            if i+1 not in allValues:
                allNotValues.append(i+1)
        
        return allNotValues

c = CollatzConjecture(27)
# q: how can i make c run on the gpu?
# a: use numba.cuda

c.random(10)
pprint.pprint(c.inorder(100000))
pprint.pprint(c.getAllNotExistentValuesAsList())
cuda.list_devices()
c.plot()