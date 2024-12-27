from re import search, match, findall
from collections import Counter, defaultdict
from itertools import product, combinations, permutations
from math import inf as INF
from math import prod
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 19
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb///6"""

DEBUG = False

cache = {}

def can_combine_towels(pattern, available, current="", depth=0):
    p.bugprint(depth*"\t", f"Trying to make {pattern}")
    if pattern == "":
        return True
    
    possible = False
    for towel in available:
        p.bugprint(depth*"\t", f"Does {pattern} start with {towel}?")
        if pattern.startswith(towel):
            key = ",".join((pattern,towel,current))
            result = cache.get(key)
            if result is None:
                result = can_combine_towels(pattern[len(towel):], available, current+towel, depth+1)
                cache[key] = result
            if result:
                possible = True
    
    return possible


def solve(data):
    count = 0

    available = data[0].split(", ")
    desired = data[2:]
    
    for pattern in desired:

        if can_combine_towels(pattern, available):
            p.bugprint("Possible!")
            count += 1
        else:
            p.bugprint("Impossible!")


    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
