import random
import time
import math
from copy import deepcopy
def readInput(n, path="input.txt"):
    # Taken from host.py
    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        last_game_field = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        game_field = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, last_game_field, game_field



def writeOutput(result, path="output.txt"):
    # Taken from host.py
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)

