from re import search, match, findall
from collections import Counter
from helpers import *
from math import prod

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3///12"""

DEBUG = True

w, h = 11, 7
SECS = 100

def solve(data):
    count = 0

    quads = [0, 0, 0, 0]
    
    for row in data:
        pos, vel = row.split(" v=")
        px, py = list(eval(pos[2:]))
        vx, vy = list(eval(vel))
        vx *= SECS
        vy *= SECS

        px = (px + vx) % w
        py = (py + vy) % h

        if px <  w // 2:
            if py < h // 2:
                quads[0] += 1
            elif py > h // 2:
                quads[1] += 1
        elif px > w // 2:
            if py < h // 2:
                quads[2] += 1
            elif py > h // 2:
                quads[3] += 1

        print(row)
        print(quads)

    return prod(quads)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        w, h = 101, 103
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
