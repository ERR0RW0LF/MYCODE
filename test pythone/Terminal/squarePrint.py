import re
from turtle import back, pos
import colorama
from colorama import Fore, Back, Style

positionX = 0
positionY = 0

def printSquare(size, positionY=0):
    colorama.init()
    
    hight = size
    width = size
    
    backColor1 = Back.RED
    backColor2 = Back.BLUE
    foreColor1 = Fore.RED
    foreColor2 = Fore.WHITE
    for i in range(hight):
        for j in range(int(width)):
            if positionY % 2 == 0:
                if j % 2 == 0:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
            else:
                if j % 2 == 0:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
        print('')
        for j in range(int(width)):
            if positionY % 2 == 0:
                if j % 2 == 0:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
            else:
                if j % 2 == 0:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
        print('')
        for j in range(int(width)):
            if positionY % 2 == 0:
                if j % 2 == 0:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
            else:
                if j % 2 == 0:
                    print(backColor2 + foreColor2 + "     ", end="" + Style.RESET_ALL)
                else:
                    print(backColor1 + foreColor1 + "     ", end="" + Style.RESET_ALL)
        print('')
        positionY += 1
    print(Style.RESET_ALL + '', end="")
    colorama.deinit()
    return positionY

'''
# Initialize colorama
colorama.init()

# Print colored text
print(Fore.RED + "This is red text")
print(Back.GREEN + "This has a green background")
print(Style.RESET_ALL + "This resets the text color and background")

# Deinitialize colorama
colorama.deinit()
'''

def main():
    positionY = 0
    positionY = printSquare(1,positionY)
    
    printSquare(2, positionY)

if __name__ == "__main__":
    main()