from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 3
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))///48"""

DEBUG = True

def mul(x, y):
    return x * y


OFF = "don't()"
ON  = "do()"

def solve(data):
    count = 0
    stuff = []
    for row in data:

        stream = ""

        on = True


        stuff += findall("don't\(\)|do\(\)|mul\(\d+,\d+\)", row)

    x = 0
                       
    for thing in stuff:
        if thing == OFF:
            on = False
        elif thing == ON:
            on = True
        elif on:
        
            x += eval(thing)
    
    return x

        



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
