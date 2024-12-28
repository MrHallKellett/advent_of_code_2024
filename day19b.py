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
bbrgwb///16"""

DEBUG = True

cache = {}
computed = {}

#bwwbrubububwugbugruuwbbwbbbbwuwruuuwbuuwbwwwgwgr
#bwwbrubububwugbugruuwbbwbbbbwuwruuuwbuuwbwwwgw


def can_combine_towels(pattern, available, current="", depth=0, count=0):



    if pattern == "":
        count += 1
        return count, False
    elif pattern in computed:
        print(f"Already know it there are {computed[pattern]} ways to make {pattern}") 
        input()
        return count * computed[pattern], False
    
    p.bugout(depth*"\t", f"Trying to make {pattern} so far i've made {current}")


    fail = True
    for towel in filter(lambda t: len(t) <= len(pattern), available):
        if pattern.startswith(towel):
            key = pattern
                        
            result = cache.get(key)
            if result is None:
                count, fail = can_combine_towels(pattern[len(towel):], available, current+towel, depth+1, count)
                cache[key] = result

    return count, fail


def solve(data):
    count = 0

    available = data[0].split(", ")
    desired = data[2:]
    
    for pattern in desired:

        this_count = can_combine_towels(pattern, available)[0]
        computed[pattern] = this_count
        
        
        count += this_count
            
            
        
            


    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
