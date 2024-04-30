import pprint
import numpy as np

test= {
    "1": {
        "t": 0,
        "y": 0,
        "x": 0
    },
    "2": { 
        "t": 1,
        "y": 1,
        "x": 1
    },
    "3": {
        "t": 2,
        "y": 2,
        "x": 2
    }
}

t1 = test["1"]
print(t1)
print(t1["t"])
t1["t"] = 1
print(t1["t"])