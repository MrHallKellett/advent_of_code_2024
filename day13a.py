from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 13
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279///480"""

DEBUG = True

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def solve(data):
    machines = [{}]

    for row in data:
        if not row:
            continue

        if "Prize" in row:
            machines.append({})
            row = row.replace("Prize: X=", "")
            x, y = map(int, row.split(", Y="))
            machines[-1]["P"] = Vector(x, y)

        else:
            for btn in "AB":
                if f"Button {btn}" in row:
                    row = row.replace(f"Button {btn}: X+", "")
                    x, y = map(int, row.split(", Y+"))
                    machines[-1][btn] = Vector(x, y)

    machines.pop(-1)

    # Summary
    # Line 1 reaches (x3,y3)(x_3, y_3)(x3​,y3​) if x3x1=y3y1\frac{x_3}{x_1} = \frac{y_3}{y_1}x1​x3​​=y1​y3​​ and t≥0t \geq 0t≥0.
    # Line 2 reaches (x3,y3)(x_3, y_3)(x3​,y3​) if x3x2=y3y2\frac{x_3}{x_2} = \frac{y_3}{y_2}x2​x3​​=y2​y3​​ and t≥0t \geq 0t≥0.
    # Line 1 and Line 2 cross before (x3,y3)(x_3, y_3)(x3​,y3​) if:
    # t1=y2⋅x2y1⋅x2−x1⋅y2≥0t_1 = \frac{y_2 \cdot x_2}{y_1 \cdot x_2 - x_1 \cdot y_2} \geq 0t1​=y1​⋅x2​−x1​⋅y2​y2​⋅x2​​≥0,
    # t2=t1⋅x1x2≥0t_2 = \frac{t_1 \cdot x_1}{x_2} \geq 0t2​=x2​t1​⋅x1​​≥0,
    # The intersection point (x,y)(x, y)(x,y) satisfies x≤x3x \leq x_3x≤x3​ and y≤y3y \leq y_3y≤y3​.


    

    for machine in machines:
        x_tot = 0
        y_tot = 0

        t = 1

        x3 = machine["P"].x
        y3 = machine["P"].y
        x1 = machine["A"].x
        y1 = machine["A"].y
        x2 = machine["B"].x
        y2 = machine["B"].y

        while t < max([x_tot, y_tot]):
            if x3 / (x1 * t) == y3 / (y3 * t):
                print("Button A




    print(machines)
    input()
        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
