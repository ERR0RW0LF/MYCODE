from pprint import pprint
import sys
import os
import json
from matplotlib import pyplot as plt

usableSymbols = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    " ",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ".",
    ",",
    "?",
    "!",
    ":",
    ";",
    "-",
    "_",
    "'",
    '"',
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "/",
    "\\",
    "|",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "+",
    "=",
    "<",
    ">",
    "~",
    "`",
    "€",
    "£",
    "¥",
    "@",
    "§",
    "°",
    "ü",
    "ö",
    "ä",
    "Ü",
    "Ö",
    "Ä",
    "ß",
    "„",
    "“",
    "”",
    "‘",
    "’",
    "‚",
    "´",
    "`",
    "«",
    "»",
    "–",
    "—",
    "…",
    "•",
    "·",
]

# q: how can i get the path of the file that i am running without the file name
# a: use os.path.dirname(os.path.realpath(__file__))

def text_analyses(text:str):
    symbols = {
        'a': 0,
    }
    for symbol in text:
        if symbol in usableSymbols:
            if symbol not in symbols:
                symbols[symbol] = 1
            else:
                symbols[symbol] += 1
    
    return symbols

def sort_dict(dict):
    new_dict = {
        0: [],
    }
    for key in dict:
        count = int(dict[key])
        if count in new_dict:
            new_dict[count].append(key)
        else:
            new_dict[count] = []
            new_dict[count].append(key)
    return new_dict

def plot_dict(dict):
    x = []
    y = []
    for key in dict:
        x.append(key)
    x.sort()
    for key in x:
        y.append(dict[key])
    
    plt.bar(x, y)
    plt.show()

if len(sys.argv) >= 2:
    paths = sys.argv[1:]
    symbolsTotal = {}
    for path in paths:
        print(path)
        if os.path.isfile(path):
            with open(path, 'r', encoding="utf8") as file:
                text = file.read()
                symbols = text_analyses(text)
                pprint(symbols)
                for symbol in symbols:
                    if symbol not in symbolsTotal:
                        symbolsTotal[symbol] = symbols[symbol]
                    else:
                        symbolsTotal[symbol] += symbols[symbol]

        else:
            print('File not found')
            sys.exit(1)
    
    plot_dict(symbolsTotal)
    
    # sort keys by value
    symbolsTotal = sort_dict(symbolsTotal)
    
    print('---'*10)
    print('Total:')
    pprint(symbolsTotal)
    
    # save to file
    print(os.path.dirname(os.path.realpath(__file__))+'\\symbolsTotal.json')
    with open(os.path.dirname(os.path.realpath(__file__))+'\\symbolsTotal.json', 'w', encoding="utf8") as file:
        json.dump(symbolsTotal, file, ensure_ascii=False, indent=4)
    
else:
    print('Usage: python textAnalyses.py <file_path>')
    sys.exit(1)
