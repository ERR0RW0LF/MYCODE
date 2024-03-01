import time
y = 0
times = input('bis zu welcher Zahl soll gezählt werden? ')
times_max = 1 + int(times)

for x in range(1, times_max):
    print(x)

for x in range(0, 10):
    print(time.time())

input('')
