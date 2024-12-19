from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 7
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20///3749"""

DEBUG = True

OPS = "*+"

def my_eval(exp):
    s = []
    o = []
    exp = exp.split(",")
    while exp:
        x = exp.pop(0)
        if x.isdigit():
            s.append(int(x))
            if len(s) == 2:
                result = eval(f"{s.pop()}{o.pop()}{s.pop()}")
                s.append(result)
        else:
            o.append(x)
    if len(s) != 1:
        raise Exception("Stack error")
    return s[0]
        
def ternarise(tot):
    

    col = 0
    while 3 ** col < tot:
        col += 1
    col -= 1
    result = ""
    while col >= 0:
        digit, tot = divmod(tot, 3**col)
        col -= 1
        result += "+*|"[digit]
    
    return result

def can_eval(target, data):
    evaluated = set()
    upper = (2 ** len(data)) - 1
    for i in range(upper):
        dcopy = list(data)
        comb = list(ternarise(i))
        exp = ""
        while dcopy:
            exp += "," + (dcopy.pop(0))
            if dcopy:
                exp += "," + (comb.pop(0))

        if exp in evaluated:
            continue
        
        if my_eval(exp) == target:

            
            return True
        
        evaluated.add(exp)
        
    return False



def solve(data):

    tot = 0
    for row in data:
        target, values = row.split(": ")
        values = values.split()
        target = int(target)
        if can_eval(target, values):
            tot += target

    return tot




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
