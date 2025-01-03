from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

# +-+-+-+-+
# |A A A A|
# +-+-+-+-+     +-+
#               |D|
# +-+-+   +-+   +-+
# |B B|   |C|
# +   +   + +-+
# |B B|   |C C|
# +-+-+   +-+ +
#           |C|
# +-+-+-+   +-+
# |E E E|
# +-+-+-+
# A = 10 x 4 = 40
# B = 8 x 4 = 32
# C = 10 x 4 = 40
# D = 4 x 1 = 4
# E = 8 x 3 = 24

# AAAA
# BBCD
# BBCC
# EEEC

# 1 0 formed a perimeter  correct
# -1 0 was out of bounds
# 1 0 formed a perimeter
# 1 1 formed a perimeter
# -1 1 was out of bounds
# 1 1 formed a perimeter
# 1 2 formed a perimeter
# -1 2 was out of bounds
# 1 2 formed a perimeter
# 0 4 was out of bounds
# 1 3 formed a perimeter
# -1 3 was out of bounds
# 1 3 formed a perimeter

DAY = 12
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """AAAA
BBCD
BBCC
EEEC///80
---RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE///1206"""



# RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE

# A region of R plants with price 12 * 18 = 216.
# A region of I plants with price 4 * 8 = 32.
# A region of C plants with price 14 * 28 = 392.
# A region of F plants with price 10 * 18 = 180.
# A region of V plants with price 13 * 20 = 260.
# A region of J plants with price 11 * 20 = 220.
# A region of C plants with price 1 * 4 = 4.
# A region of E plants with price 13 * 18 = 234.
# A region of I plants with price 14 * 22 = 308.
# A region of M plants with price 5 * 12 = 60.
# A region of S plants with price 3 * 8 = 24.

DEBUG = True

NEIGHBOURS = ((1, 0), (0, 1), (-1, 0), (0, -1))
H, W = None, None

def out_of_bounds(yn, xn):
    return yn < 0 or yn > H-1 \
        or xn < 0 or xn > W-1

def is_perim(yn, xn, data, plant):
    
    
    for yc, xc in NEIGHBOURS:
        #print("checking", yc, xc)
        
        yn2, xn2 = yn+yc, xn+xc
    
    
        
        if out_of_bounds(yn2, xn2) \
        or data[yn2][xn2] != plant:
            return True
            
            
    return False

def explore_region(data, pos, visited, plant=None, perim=0, area=1, considered_perim=None):

    if considered_perim is None:
        considered_perim = set()

    y, x = pos

    visited.add((y, x))

    if plant is None:
        plant = data[y][x]
        if is_perim(y, x, data, plant):
            considered_perim.add((y, x))


    for yc, xc in NEIGHBOURS:

        yn, xn = y+yc, x+xc
        here = (yn, xn)
        if here in visited or out_of_bounds(yn, xn):
        
            continue
        

        if data[yn][xn] == plant:
            visited.add(here)
            area += 1

            if is_perim(yn, xn, data, plant):
                considered_perim.add((yn, xn))
            
            visited, perim, area, considered_perim = explore_region(data, here, visited, plant, perim, area, considered_perim)



    return visited, area, considered_perim

def calculate_sides(considered):
    considered = list(considered)
    print(considered)
    input()
    y, x, yc, xc = considered.pop(0)
    print(f"I'll start at {y} {x} heading {yc}{xc}")
    sides = 1
    while considered:
        try: # to walk along the same side in direction headed
            yn = y + yc
            xn = x + xc
            considered.remove((yn, xn, yc, xc))
            
            y = yn
            x = xn
            print(f"Continue to {y} {x} still heading {yc}{xc}")
            continue
        except ValueError:
            i = NEIGHBOURS.index((yc, xc))
            perim_found = False
            # try same square, but different direction
            for j in range(i+1, i+3):
                if perim_found: continue
                i = i % 4
                ycn, xcn = NEIGHBOURS[i]
                print(f"Let's try direction {ycn}{xcn}")
                try:
                    considered.remove((y, x, ycn, xcn))
                    perim_found = True
                    yc = ycn
                    xc = xcn
                    print(f"Turned a corner at {y} {x} now heading {yc}{xc}")
                    sides += 1
                    continue
                except ValueError:
                    pass
            if not perim_found:
                raise Exception("Perimeter error")


    
    
def solve(data):
    global H, W
    H = len(data)
    W = len(data[0])
    tot = 0
    visited = set()
    for y, row in enumerate(data):
        for x, plant in enumerate(row):
            if (y, x) not in visited:
                visited, area, considered = explore_region(data, (y, x), visited)
                print(f"Explored the {data[y][x]} region")
                
                
                
                sides = calculate_sides(considered)
                print(sides, "sides found")
                input()
                
                tot += sides * area

    return tot




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
