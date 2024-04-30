import sys
import os
import numpy as np
import json

def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

