from re import search, match, findall
from collections import Counter, defaultdict
from helpers import *
from math import inf as INF
from itertools import combinations

PP_ARGS = False, False #rotate, cast int

DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............///34"""

DEBUG = True

class VectorSet(set):
    def __contains__(self, check):
        return any([check.x == v.x and check.y == v.y \
                   for v in self])
    
    def append(self, item):
        self.add(item)
        
    def __hash__(self):
        sorted_vectors = sorted(self, key=lambda v: (v.x, v.y))
        return hash(tuple((v.x, v.y) for v in sorted_vectors))
    
    def __eq__(self, other):
        return all(v.x == o.x and v.y == o.y for v, o in zip(self, other))
    
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
    
    def __hash__(self):
        return hash(f"{self.x,self.y}")
    
    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y

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
    antennae = defaultdict(VectorSet)
    antinodes = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell != ".":
                antennae[cell].append(Vector(x, y))


    

    for symbol, antenna_list in antennae.items():
        print(f"Processing {symbol}")
        antenna_pairs = set(VectorSet(p) for p in combinations(antenna_list, 2))

        while antenna_pairs:
            print("antenna loop")
            a1, a2 = list(antenna_pairs.pop())
            diff = a1.diff(a2)
            new1 = a1.find_line(diff, a2)
            new2 = a2.find_line(diff, a1)
            
            for new in (new1, new2):
                if 0 <= new.y < h:
                    if 0 <= new.x < w:
                        newly_added = True
                        newv = Vector(new.x, new.y)
                        if newv in antennae[symbol]:
                            continue
                        
                        antennae[symbol].add(newv)
                        data[new.y][new.x] = "#"

                        for a in antenna_list:
                            if a == newv:   continue
                            this_comb = VectorSet((newv, a))
                            print(len(antenna_pairs), "pairs before")
                            print(f"adding\n{this_comb}\nto:")
                            
                            antenna_pairs.add(this_comb)
                            print(len(antenna_pairs), "pairs after")
                
            display(data)
            


    

        
    

    return sum(row.count("#") for row in data)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
