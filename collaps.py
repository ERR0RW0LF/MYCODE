x = int(input("Zahl: "))
list = []

while x != 1:
    if (x % 2) == 0:
        x = x / 2
    else:
        x = x * 3 + 1
    print(x)
    list.append(x)

print("Ende")

print(list)

input()