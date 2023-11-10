import math as ma

a = 0
b = 0
c = 0
d = 0

a = input('a: ')
b = input('b: ')
c = input('c: ')

rechneart = input('Btte geben sie die gewünschte Rechen Art an(Plus: +; Minus: -; Mall: *; Geteild: /): ')

if rechneart == '+':
    d = int(a)+int(b)+int(c)
    print(d)
elif rechneart == '-':
    d = int(a) - int(b) - int(c)
    print(d)
elif rechneart == '*':
    d = int(a) * int(b) * int(c)
    print(d)
elif rechneart == '/':
    d = int(a) / int(b) / int(c)
    print(d)
else:
    print('errore')

input('Drücke eine Taste zum benden: ')
