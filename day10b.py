from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9///2
---10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01///3
---89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732///36"""

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DEBUG = True

def show_map(display, graph, y, x):
    display[y][x] = graph[y][x]

    for row in display:
        for col in row:
            print(col, end="")
        print()

    print()

def dfs(graph, start, tot):
    
    H = len(graph)
    W = len(graph[0])
    display = [["." for _ in range(W)] for _ in range(H)]
    peaks = set()
    visited = set()
    q = [start]
    #print(f"starting hiking from {start}")
    while len(q):
        y, x = q.pop(0)
        visited.add((y, x))
        #show_map(display, graph, y, x)
        #input()
        for x2, y2 in DIRECTIONS:
            nx = x + x2
            ny = y + y2
            here = (ny, nx)
            if here not in visited:
                if 0 <= ny < H:
                    if 0 <= nx < W:
                        new = graph[ny][nx]
                        prev = graph[y][x]
                        if new != "." and prev != ".":
                            if int(new) - int(prev) == 1:
                                q.append(here)
                                if new == '9':
                                    peaks.add(here)
        
    count = len(peaks)
    #print(f"Found {count} peaks!")                
    
    return count

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

        
