from re import search, match, findall
from collections import Counter, defaultdict
from itertools import product, combinations, permutations
from math import inf as INF
from math import prod
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 18
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0///(6, 1)"""

DEBUG = True

def display(blocked, path):
    s = ""
    for y in range(h):
        for x in range(w):
            if (x, y) in blocked:
                s += "#"
            elif (x, y) in path:
                s += "X"
            else:
                s += "."
        s += "\n"
    print(s)
    input()

def solve(data):
    start = 0, 0
    destination = w-1, h-1
    blocked = set(eval(row) for row in data[:bytes])    
    grid = []
    [[grid.extend([(x, y)]) for y in range(h)] for x in range(w)]
    
    for byte_counter in range(bytes, len(data)):
        print(f"Adding byte {byte_counter}")
        newest_byte = eval(data[byte_counter])
        blocked.add(newest_byte)
        if traverse(blocked, newest_byte, start, destination, grid) == INF:
            return newest_byte

def traverse(blocked, newest_byte, start, destination, grid):
    start, destination = destination, start
    
    distances = defaultdict(lambda: INF)
    distances[start] = 0
    prev = defaultdict(lambda: None)
    current = None
    
    unvisited = set(coord for coord in grid if coord not in blocked)
    
    
    explore = True
    while explore:
        current = min(unvisited, key=lambda x: distances[x])
        unvisited.remove(current)

        for x, y in ((0, 1), (-1, 0), (0, -1), (1, 0)):
            ny, nx = current[1]+y, current[0]+x
            if nx < 0 or nx >= w or ny < 0 or ny >= h:
                continue

            neighbour = nx, ny

            if neighbour not in blocked:

                
                if distances[current] < distances[neighbour]:
                    distances[neighbour] = distances[current] + 1
                    prev[neighbour] = current
        

        if not unvisited:
            explore = False 

    return distances[destination]




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    w, h = 7, 7
    bytes = 12
    if p.check(TESTS, solve):
        w, h = 71, 71
        bytes = 1024
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
