from re import search, match, findall
from collections import Counter, defaultdict
from itertools import product, combinations, permutations
from math import inf as INF
from math import prod
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0///4,6,3,5,6,3,5,2,1,0"""

DEBUG = True




def solve(data, testing=False):

    

    count = 0

    a = int(data[0].split("A: ")[1])
    b = int(data[1].split("B: ")[1])
    c = int(data[2].split("C: ")[1])

    prog = data[-1].replace("Program: ", "").split(",")

    outputs = []

    ip = 0

    halt = False
    while not halt:
        try:
            opcode = int(prog[ip])
            operand = int(prog[ip+1])
        except IndexError:
            print("Halt due to ip")
            halt = True
            continue

        print(f"Executing opcode {opcode} with operand {operand}")
        literal = operand
        if operand < 4:
            combo = operand
        elif operand >= 7:
            combo = None
        else:
            combo = [a,b,c][operand-4]

        if opcode == 0:
            a = int(a / 2**combo)
        elif opcode == 1:
            b = b ^ literal
        elif opcode == 2:
            b = combo % 8
        elif opcode == 3:
            if a != 0:
                ip = literal
                continue
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            out = combo % 8
            outputs.append(str(out))
        elif opcode == 6:
            b = int(a / 2**combo)
        elif opcode == 7:
            c = int(a / 2**combo)
        else:
            print("Halt due to illegal opcode")
            halt = True

        ip += 2
    

    final =  ",".join(outputs)
    print(final)

    if testing:
        print(f"final out {final}\nfinal registers a: {a} b: {b} c: {c}")
        return final, [a, b, c]

    return final


def unit_tests():
    
    
    print("If register C contains 9, the program 2,6 would set register B to 1.")
    data = '''Register A: 0
Register B: 0
Register C: 9

Program: 2,6'''.splitlines()
    output, registers = solve(data, testing=True)
    assert registers[1] == 1

    print("If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.")
    data = '''Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4'''.splitlines()
    output, registers = solve(data, testing=True)
    assert output == "0,1,2"

    print("If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.")


    # 0,1,5,4,3,0
    # opcode 0, operand 1
    # opcode 5, operand 4
    # opcode 3, operand 0

    data = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0'''.splitlines()
    output, registers = solve(data, testing=True)
    assert output == "4,2,5,6,7,7,7,7,3,1,0"
    assert registers[0] == 0

    print("If register B contains 29, the program 1,7 would set register B to 26.")
    data = '''Register A: 0
Register B: 29
Register C: 0

Program: 1,7'''.splitlines()
    output, registers = solve(data, testing=True)
    assert registers[1] == 26

    print("If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.")
    data = '''Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0'''.splitlines()
    output, registers = solve(data, testing=True)
    assert registers[1] == 44354
    


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    unit_tests()
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
