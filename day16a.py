from re import search, match, findall
from collections import Counter, defaultdict
from helpers import *
from math import inf as INF

PP_ARGS = False, False #rotate, cast int

DAY = 16
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############///11048"""

DEBUG = True



def solve(data):
    count = 0
    maze = {}
    w, h = len(data[0]), len(data)

    display([], data)

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "#":
                continue

            neighbours = list(get_neighbours(data, y, x))
            vertex = False
            if len(neighbours) > 2:
                vertex = True
            elif len(neighbours) == 2:
                n1, n2 = neighbours
                if n1[0] != n2[0] and n1[1] != n2[1]:
                    vertex = True

            if vertex:
                node = get_or_make_node((y, x), maze)
                if cell == "S":
                    start = node
                elif cell == "E":
                    end = node
    
    display(maze.values(), data)
    input()

    def connect_vertices(node, data, maze):

        for yv, xv in ((1, 0), (0, 1),
                       (-1, 0), (0, -1)):
            y, x = node.data
            track = True
            count = 1
            while track:
                y += yv
                x += xv

                if data[y][x] == "#":
                    track = False
                elif (y, x) in maze.keys():
                    neighbour = maze[(y, x)]
                    if y == node.data[0]:
                        direction = ">"
                    elif x == node.data[1]:
                        direction = "^"
                    
                    node.add_connection(neighbour, count, extra=direction)

                    track = False
                else:
                    count += 1

    for node in maze.values():
        connect_vertices(node, data, maze)



    path, cost = a_star(start, end, manhattan)

    

    print("Best path is", path)
    print(len(path), "steps", f"cost {cost}")

    display(path, data)
    input()





def display(path, data):
    w, h = len(data[0]), len(data)
    s = ""
    print("   " + "".join(chr(i+48) for i in range(w)))
    for y, row in enumerate(data):
        s += chr(y+48).ljust(3)
        for x, cell in enumerate(row):
            for node in path:
                if (y, x) == node.data:
                    cell = "^"
                    break
            s += cell
        s += "\n"
    print(s)

def manhattan(p1, p2):
    y1, x1 = p1.data
    y2, x2 = p2.data
    return abs(x2-x1) + abs(y2-y1)

def reconstruct_path(came_from, current):
    total_path = []
    cost = 0
    while current in came_from.keys():
        current, this_cost = came_from[current]
        cost += this_cost
        total_path = [current] + total_path
    return total_path, cost

def a_star(start, goal, h):
    open_set = set([start])
    came_from = {}
    g_score = defaultdict(lambda: INF)
    g_score[start] = 0
    f_score = defaultdict(lambda: INF)
    f_score[start] = h(start, goal)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        print(f"Chose {current} as the next current node")
        
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        for key, connection in current.connections.items():
            
            neighbour, weight, direction = connection
            
            print(f"Found neighbour of {current} at {neighbour}. Costs {weight} to get there")
            
            if current in came_from and direction != came_from[current]:
                weight += 1000            

            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current, direction
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + h(neighbour, goal)
                if neighbour not in open_set:
                    open_set.add(neighbour)

    raise Exception("A star failure")


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
