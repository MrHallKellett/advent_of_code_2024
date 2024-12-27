from re import search, match, findall
from collections import Counter, defaultdict
from itertools import product, combinations, permutations
from math import inf as INF
from math import prod
from helpers import *
from multiprocessing import Pool
from os import cpu_count

PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0///117440"""

DEBUG = True


# 3,0,7,5,0,3,0,4,0,7,3,1
# 2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0




def solve(*args):
    print("Received these args", args, len(args[0]))
    if len(args[0]) != 3:
        print("1 arg")
        data = args[0]
        start = 100000
        end   = 999999
    else:
        
        data, start, end = args[0]

    

    count = 0

    a = int(data[0].split("A: ")[1])
    b = int(data[1].split("B: ")[1])
    c = int(data[2].split("C: ")[1])

    prog = data[-1].replace("Program: ", "").split(",")

    final = ""

    for a_rep in range(start, end):
        a = a_rep

        outputs = []

        ip = 0

        halt = False
        iter_counter = 0
        while not halt:
            iter_counter += 1
            if iter_counter > 1000:
                print("infinite")
                break
            try:
                opcode = int(prog[ip])
                operand = int(prog[ip+1])
            except IndexError:
                
                halt = True
                continue

            
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
                
                halt = True

            ip += 2
        
        if a_rep % 1000 == 0:
            print("Tested", a_rep) 

        final =  ",".join(outputs)

        if final == ",".join(prog):
            return a_rep



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    
    if p.check(TESTS, solve):
        input()
        start = 100000000000000
        end   = 999999999999999

        tasks = []
        num_workers = cpu_count() * 10
        diff = end - start
        chunk = diff // num_workers

        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)

        for i in range(num_workers):
            this_start = start + (chunk * i)
            this_end = this_start + chunk
            tasks += [(this_start, this_end)]
            print(f"Spawning a worker that will run from {this_start} to {this_end}")

        print("POTENTIAL FINAL ANSWER:")
        with Pool(5) as pool:
            print(pool.map(solve, [(puzzle_input, start, end) for start, end  in tasks]))

        
        
