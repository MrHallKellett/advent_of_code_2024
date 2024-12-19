from re import search, match, findall
from collections import Counter
from helpers import *
from uuid import uuid4

PP_ARGS = False, False #rotate, cast int

DAY = 11
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """125 17///55312"""
BLINKS_REQ = 25

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


stones = []

class Stone:
    def __init__(self, value):
        stones.append(self)
        self.engraving = value
        self.next = None
        self.prev = None
        self.resolve_prev = None
        self.resolve_next = None
        self.resolve_engraving = None
        self.id = uuid4().hex

    def __repr__(self):
        return self.id

    def init_blink(self):
        num = str(self.engraving)
        length = len(num)
        if num == '0':
            
            self.resolve_engraving = 1
        elif length % 2 == 0:
            
            # new value for me
            self.resolve_engraving = int(num[:length//2])
            # new stone for the right
            self.resolve_next = Stone(int(num[length//2:]))
            # my new next links to my old next
            self.resolve_next.next = self.next
            
        else:
            
            self.resolve_engraving = int(num) * 2024
        
    def finish_blink(self):
        if self.resolve_engraving:
            self.engraving = self.resolve_engraving
            self.resolve_engraving = None
         
        # if i have a new next...
        if self.resolve_next:
            # if i had a next
            if self.next:
                # my old next links back to my new next
                self.next.prev = self.resolve_next
        
            # i link to my new next
            self.next = self.resolve_next
            # my new next links back to me
            self.next.prev = self

            self.resolve_next = None
            
            
    
def count_stones(headstone, display=True):
    stone = headstone
    
    count = 0
    while stone is not None:
        if display:
            print(stone.engraving, end=" ")
        count += 1
        stone = stone.next
        
        

    return count

def blink_stones(headstone):
    stone = headstone
    while stone is not None:
        stone.init_blink()
        stone = stone.next
    stone = headstone
    while stone is not None:
        stone.finish_blink()
        stone = stone.next

    # for s in stones:
    #     print(s, "links back to", s.prev)
    #     print(s, "links forward to", s.next)

def init_stones(data):
    headstone = None
    prev = None
    next = None
    for num in data:
        this_stone = Stone(num)
        if prev is not None:
            prev.next = this_stone
            this_stone.prev = prev
        if headstone is None:
            headstone = this_stone

        prev = this_stone
    return headstone

def solve(data):
    headstone = init_stones(list(map(int, data[0].split())))

    for blink_no in range(BLINKS_REQ+1):
        print(f"After {blink_no} blinks")
        count = count_stones(headstone, display=False)
        print(count)
        blink_stones(headstone)
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
