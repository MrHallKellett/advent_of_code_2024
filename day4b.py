from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 4
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX///9"""



DEBUG = True





def solve(data):
    count = 0

    W = len(data[0])
    H = len(data)
        
    def cross(d, x, y):

        return d[y][x] == "A" and \
        ((d[y-1][x-1] == "M" and d[y-1][x+1] == "M" and \
        d[y+1][x-1] == "S" and d[y+1][x+1] == "S") or \
        \
        (d[y-1][x-1] == "M" and d[y-1][x+1] == "S" and \
        d[y+1][x-1] == "M" and d[y+1][x+1] == "S") or \
        \
        (d[y-1][x-1] == "S" and d[y-1][x+1] == "M" and \
        d[y+1][x-1] == "S" and d[y+1][x+1] == "M") or \
        \
        (d[y-1][x-1] == "S" and d[y-1][x+1] == "S" and \
        d[y+1][x-1] == "M" and d[y+1][x+1] == "M") )

    # tidy later
    data = NoNegList(NoNegList(row) for row in data)

    for y in range(H):
        for x in range(W):
            try:
                if cross(data, x, y):
                    count += 1
            except IndexError:
                pass

   

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
