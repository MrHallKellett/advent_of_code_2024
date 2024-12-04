from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 2
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9///4"""

DEBUG = True


def solve(data):
    count = 0
    
    for row2 in data:

        row2 = list(map(int, row2.split()))

        for i in range(len(row2)):

            row = list(row2)

            row.pop(i)

            safe = True
            if sorted(row) == row or sorted(row, reverse=True) == row:
                for i, x in enumerate(row[:-1]):
                    
                    diff = abs(x - row[i+1])
                    if diff > 3 or diff < 1:
                
                        safe = False
            else:
                safe = False
            if safe:                
                count += 1
                break
            
                
            

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
