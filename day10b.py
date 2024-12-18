from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....///3
---89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732///81"""

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DEBUG = False

def show_map(display, graph, y, x):
    display[y][x] = graph[y][x]

    for row in display:
        for col in row:
            p.bugprint(col, end="")
        p.bugprint()

    p.bugprint()

def dfs(graph, start, tot):
    
    H = len(graph)
    W = len(graph[0])
    display = [["." for _ in range(W)] for _ in range(H)]
    peaks = 0
    visited = set()
    s = [start]
    p.bugprint(f"starting hiking from {start}")
    while len(s):
        y, x = s.pop(-1)
        
        #visited.add((y, x))
        
        show_map(display, graph, y, x)
        
        for x2, y2 in DIRECTIONS:
            nx = x + x2
            ny = y + y2
            
            if 0 <= ny < H:
                if 0 <= nx < W:
                    here = (ny, nx)
                    if here not in visited:
                        new = graph[ny][nx]    
                        prev = graph[y][x]
                        if new != "." and prev != ".":
                            if int(new) - int(prev) == 1:
                                s.append(here)
                                if new == '9':
                                    peaks += 1
        
    
    print(f"Found {peaks} peaks!")                
    
    return peaks

def solve(data):
    tot = 0

    data = [list(row) for row in data]

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == '0':
                tot += dfs(data, (y, x), tot)
                #input(f"tot is now {tot}")

        
    

    return tot




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
