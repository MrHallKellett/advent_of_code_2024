from re import search, match, findall
from collections import Counter
from helpers import *
from math import prod

from colorama import init, Fore


init()

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
SECS = 200000

COLOURS = ((255, 255, 255), 
           (0, 100, 0), 
           (100, 0, 0), 
           (0, 0, 100), 
           (100, 100, 0), 
           (0, 100, 100), 
           (100, 0, 100), 
           )


COLOURS = Fore.WHITE, Fore.GREEN, Fore.RED, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW

seq = []

def write_image(second, robots):

    grid = [[0 for _ in range(w)] for _ in range(h)]

    for robot in robots:
        grid[robot.py][robot.px] += 1
            

    
    s = "\n".join("".join([COLOURS[i] + "█" for i in row]) for row in grid)
            
    
    print(s)
    seq.append(hash(s))

    if len(seq) > 20:
        for i in range(0, len(seq)-3):
            if seq[i:i+3] == seq[-3:]:
                print("periodicity found")
                f.close()
                exit()

    print(f"outputted second {second}")  
    input()


class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def move(self):
        self.px = (self.px + self.vx) % w
        self.py = (self.py + self.vy) % h

    def here(self, x, y):
        return self.px == x and self.py == y

def display(second, robots):
    print(second)
    s = ""
    for y in range(h):
        for x in range(w):
            cell = [robot.here(x, y) for robot in robots].count(True)
            s += str(cell) if cell else " "
        s += "\n"
    
    print(s)
    print()
    input()

def solve(data):
    count = 0

    quads = [0, 0, 0, 0]
    
    robots = []
    for row in data:
        pos, vel = row.split(" v=")
        px, py = list(eval(pos[2:]))
        vx, vy = list(eval(vel))
        robots.append(Robot(px, py, vx, vy))


    for second in range(1, SECS):
        
        for robot in robots:
            
            robot.move()

        if (second - 98) % w == 0:
            write_image(second, robots)


    

    




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if True: #p.check(TESTS, solve):
        w, h = 101, 103
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
