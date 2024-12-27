from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 15
TEST_DELIM = "---"
FILE_DELIM = "\n"

TESTS = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^///9021"""

DEBUG = True

def display(warehouse, robot):
    if not p.debug:
        return
    s = ""
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if x == robot.x and y == robot.y:
                s += "@"
            else:
                s += cell
        s += "\n"
    print(s)
    
    #p.buginput()
    print()
    return s

def calculate_total_gps(warehouse):
    total = 0
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell == "O":
                total += 100 * y + x
    return total

def solve(data, convert=True, unit_testing=False):
    
    warehouse = []
    mazing = True
    directions = []
    robot = 0, 0
    for y, row in enumerate(data):
        if convert:
            for orig, rep in (("#", "##"),
                            ("O", "[]"),
                            (".", ".."),
                            ("@", "@.")):
                row = row.replace(orig, rep)

        adjust = 1 if convert else 0 
            
        if "@" in row:
            robot = Vector(row.index("@")+adjust, y)
            row = row.replace("@", ".")
        if not row:
            mazing = False
            continue
        if mazing:
            warehouse.append(list(row))
        else:
            directions.extend(list(row))

    print(warehouse)
    print(directions)
    print(robot)

    display(warehouse, robot)

    def move_box(warehouse, bx, by, vx, vy):
        p.bugprint(f"move boxes from {by} {bx}")
        ox, oy = bx, by

        track = True
        boxing = True
        box_line, spaces = 0, False
        current_box_part = None
        while track:
            cell = warehouse[by][bx]
            ax = None
            try:              
                ax = {"[":1, "]":-1}[current_box_part]
                print(f'ax is now {ax}')
            except KeyError:
                pass
            if cell == "#":
                track = False
            elif vy and ax and warehouse[by][bx+ax] == "#":
                print("New check")
                track = False
            elif cell in '[]':
                current_box_part = cell
                if boxing:
                    box_line += 1
                else:
                    track = False
            else:
                boxing = False
                if cell == '.':
                    spaces = True
                    track = False
            
            bx += vx
            by += vy

        p.bugprint(f"found {box_line} boxes in front and {spaces} spaces")
        y, x = oy, ox
        p.bugprint(f"before: {warehouse[y]}")
        if spaces:
            for i in range(box_line, 0, -1):
                y = oy + vy * i
                x = ox + vx * i
                
                ax = None
                if warehouse[y-vy][x-vx] == "[":
                    ax = 1
                    print("need to consider right half of box")
                elif warehouse[y-vy][x-vx] == "]":
                    ax = -1
                    print("need to consider left half of box")


                warehouse[y][x], warehouse[y-vy][x-vx] = \
                warehouse[y-vy][x-vx], warehouse[y][x]

                if vy: # if going vertical
                    if ax:
                        # also adjust other half of box
                        warehouse[y][x+ax], warehouse[y-vy][x-vx+ax] = \
                        warehouse[y-vy][x-vx+ax], warehouse[y][x+ax]




        else:
            pass
            p.bugprint("No space to move")
            

        p.bugprint(f"after: {warehouse[y]}")

        return spaces, warehouse
            
    w, h = len(warehouse[0]), len(warehouse)

    while directions:
        direction = directions.pop(0)
        print(f"Move {direction}:")
        if direction == ">":
            vx, vy = 1, 0
        elif direction == "<":
            vx, vy = -1, 0
        elif direction == "^":
            vx, vy = 0, -1
        else:
            vx, vy = 0, 1
        
        nx, ny = robot.x + vx, robot.y + vy
        if 0 <= nx < w:
            if 0 <= ny < h:
                in_front = warehouse[ny][nx]
                if in_front == "#":
                    pass
                else:
                    moves = 1
                    if in_front in '[]':
                        
                        moves, warehouse = move_box(warehouse, nx, ny, vx, vy)
                    print(moves, "moves made")
                    robot.x += vx * moves
                    robot.y += vy * moves


        displayed = display(warehouse, robot) 
        if any(illegal in displayed for illegal in "[.,.],[#,#]".split(",")):
            raise Exception("oops, broken box")

    if unit_testing:
        return displayed
    
    


    return calculate_total_gps(warehouse)

def unit_tests():

    

    with open("day15b.tests") as f:
        data = f.read().split("\n///\n")

    for test in data:
        inp, out = test.split("out:")
        inp = inp.replace("in:\n", "")
        displayed = solve(inp.splitlines(), convert=False, unit_testing=True)

        displayed = displayed.strip()
        out = out.strip()
        print(displayed)
        print("vs\n")
        print(out)
        print(len(displayed), "vs", len(out))
        
        if out != displayed:
            assert False


    
    return True

        
        




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)


    if unit_tests():
        if p.check(TESTS, solve):
            puzzle_input = p.load_puzzle()
            puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
            print("FINAL ANSWER: ", solve(puzzle_input))

        
