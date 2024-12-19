from re import search, match, findall
from collections import Counter
from helpers import *
from uuid import uuid4

PP_ARGS = False, False #rotate, cast int

DAY = 11
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """125 17///55312"""
BLINKS_REQ = 75

'''If the stone is engraved with the number 0,
it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has
an even number of digits, it is replaced by two stones.
The left half of the digits are engraved on the new left
stone, and the right half of the digits are engraved on
the new right stone. (The new numbers don't keep extra
leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced
by a new stone; the old stone's number multiplied by
2024 is engraved on the new stone.'''

DEBUG = True


def solve(data):
    stones = Counter(map(int, data[0].split()))
    
    for blink_no in range(BLINKS_REQ):
        for stone, amt in Counter(stones).items():
            strone = str(stone)
            leng = len(strone)
            
            if stone == 0:
                stones[1] += amt
            elif leng % 2 == 0:
                left = int(strone[:leng//2])
                right = int(strone[leng//2:])
                stones[left] += amt
                stones[right] += amt
            else:
                stones[stone*2024] += amt
                
            stones[stone] -= amt
            if stones[stone] == 0:
                stones.pop(stone)
        #print(f"After {blink_no+1} blinks:")
        #print(stones)
        #print(sum(stones.values()), "stones total")
        #input()

       
    return sum(stones.values())




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if True: #p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
