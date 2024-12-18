from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 9
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """2333133121414131402///1928"""

DEBUG = True
def decompress(data):
    result = []
    for i in range(0, len(data), 2):
        val = i // 2
        result.extend([val for _ in range(data[i])])
        try:
            result.extend([None] * data[i+1])
        except IndexError:
            pass

    return result

def defragment(data):
    while None in data:
        fill = data.index(None)
        move = data.pop(-1)
        if move is not None:
            data[fill] = move
            print(f"moved {move} to {fill}")

    return data

def checksum(data):
    return sum([i*j for i, j in enumerate(data)])

def solve(data):
    data = data[0]
    data = list(map(int, list(data)))
    data = decompress(data)
    data = defragment(data)
    return checksum(data)

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
