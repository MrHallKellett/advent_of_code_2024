from re import search, match, findall
from collections import Counter
from helpers import *
from itertools import product 

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
292: 11 6 16 20///11387"""

DEBUG = False

OP_CHOICES = "*+|"
MAX_OPS = 15

def my_eval(exp):
    s = []
    o = []
    exp = exp.split(",")
    exp.remove("")
    while exp:
        p.bugprint("expression", exp)
        x = exp.pop(0)
        p.bugprint("values stack", s)
        p.bugprint("op stack", o)
        #input()
        if x.isdigit():
            s.append(int(x))
            if len(s) == 2:
                sub_exp = f"{s.pop(0)}{o.pop()}{s.pop(0)}"
                p.bugprint("Found exp", sub_exp)
                if "|" in sub_exp:
                    result = int(sub_exp.replace("|", ""))
                else:
                    result = eval(sub_exp)
                s.append(result)
                p.bugprint("Computed result it's", result)
                p.buginput()
        else:
            o.append(x)
    if len(s) != 1:
        raise Exception("Stack error")
    return s[0]
        


def can_eval(target, data, combs):
    evaluated = set()
    upper = 3 ** (len(data) - 1)
    p.bugprint(f"{target}: {' '.join(str(i) for i in data)}")


    p.bugprint("Counting up to", upper)
    p.buginput()
    for i in range(upper):
        dcopy = list(data)
        comb = list(combs[i])
        
        #print(f"Combination from {i} is", comb)
        p.buginput()
        exp = ""
        while dcopy:
            exp += "," + (dcopy.pop(0))
            if dcopy:
                exp += "," + (comb.pop(-1))

        if exp in evaluated:
            continue

        
        
        if my_eval(exp) == target:
            p.bugprint(f"can be made true through {exp.replace(',', '')}")         
            return True
        
        evaluated.add(exp)
    
    
    p.bugprint("cannot be made true")
    return False



def solve(data):

    OP_COMBS = list(product(OP_CHOICES, repeat=MAX_OPS))

    tot = 0
    for row in data:
        target, values = row.split(": ")
        values = values.split()
        target = int(target)
        if can_eval(target, values, OP_COMBS):
            tot += target

    return tot




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
