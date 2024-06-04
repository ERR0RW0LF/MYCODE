from pprint import pprint
import sys
import os

# q: how can i get the path of the file that i am running without the file name
# a: use os.path.dirname(os.path.realpath(__file__))

def text_analyses(text:str):
    symbols = {
        'a': 0,
    }
    for symbol in text:
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
    
    # sort keys by value
    symbolsTotal = sort_dict(symbolsTotal)
    
    print('---'*10)
    print('Total:')
    pprint(symbolsTotal)
    
    # save to file
    print(os.path.dirname(os.path.realpath(__file__))+'\\symbolsTotal.txt')
    with open(os.path.dirname(os.path.realpath(__file__))+'\\symbolsTotal.txt', 'w', encoding="utf8") as file:
        file.write(str(symbolsTotal))
    
else:
    print('Usage: python textAnalyses.py <file_path>')
    sys.exit(1)