from re import search, match, findall
from collections import Counter, defaultdict
from helpers import *
from math import inf as INF
from itertools import combinations

PP_ARGS = False, False #rotate, cast int

DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """..........
..........
..........
....a.....
........a.
.....a....
..........
..........
..........
..........///4---............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............///14"""

DEBUG = True

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def diff(self, other):
        return Vector(abs(self.x-other.x), abs(self.y-other.y))
    
    def inverse(self):
        return Vector(0-self.x, 0-self.y)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __repr__(self):
        return f"x {self.x}, y {self.y}"

    def find_line(self, diff, other):
        if self.x < other.x:
            x = self.x - diff.x
        else:
            x = self.x + diff.x

        if self.y < other.y:
            y = self.y - diff.y
        else:
            y = self.y + diff.y

        return Vector(x, y)



def display(data):
    print("   " + "".join(hex(i)[2:] for i in range(len(data[0]))))
    for y, row in enumerate(data):
        print(str(y) + "  " + "".join(row))

def solve(data):
    count = 0

    data = [list(row) for row in data]

    h = len(data)
    w = len(data[0])

    display(data)
    input()
    antennae = defaultdict(list)
    antinodes = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell != ".":
                antennae[cell].append(Vector(x, y))

    for symbol, antenna_list in antennae.items():
        for a1, a2 in combinations(antenna_list, 2):
            diff = a1.diff(a2)
            new1 = a1.find_line(diff, a2)
            new2 = a2.find_line(diff, a1)
            
            if 0 <= new1.y < h:
                if 0 <= new1.x < w:
                    data[new1.y][new1.x] = "#"
            if 0 <= new2.y < h:
                if 0 <= new2.x < w:
                    data[new2.y][new2.x] = "#"
            
            # display(data)


    

        
    

    return sum(row.count("#") for row in data)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
