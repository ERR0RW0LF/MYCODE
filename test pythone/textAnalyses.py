from pprint import pprint
import sys
import os



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
                symbolsTotal[path] = symbols

        else:
            print('File not found')
            sys.exit(1)
    
    pprint(symbolsTotal)
else:
    print('Usage: python textAnalyses.py <file_path>')
    sys.exit(1)