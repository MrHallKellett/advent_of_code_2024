from re import search, match, findall
from collections import Counter
#from pyproj import Geod
#from shapely import wkt
#import networkx as nx 
#import matplotlib.pyplot as plt 

GREEDY = "\[.+\]" # greedily match anything between [ and ]
LAZY = "\[.+?\]"  # lazily match anything between [ and ]

def is_iterable(seq):
    try:
        [i for i in seq]
        return True
    except TypeError:
        return False

class NoNegList(list):
    """A  [nested] list that does not permit negative indexing"""
    def __init__(self, data):
        if self[:]:
            pass # TODO, recurse - allow nested thingies
        
    def __getitem__(self, key):        
        
        if key < 0:
            raise IndexError
        else:
            return super().__getitem__(key)
        
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def diff(self, other):
        return Vector(abs(self.x-other.x), abs(self.y-other.y))
    
    def inverse(self):
        return Vector(0-self.x, 0-self.y)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __repr__(self):
        return f"x {self.x}, y {self.y}"

    def find_line(self, diff, other):
        if self.x < other.x:
            x = self.x - diff.x
        else:
            x = self.x + diff.x

        if self.y < other.y:
            y = self.y - diff.y
        else:
            y = self.y + diff.y

        return Vector(x, y)

def get_neighbours(grid: list, y:int, x:int, diag: bool=False, blocked="#"):
    w, h = len(grid[0]), len(grid)
    coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if diag:
        coords.insert(1, (1, 1))
        coords.insert(3, (-1, 1))
        coords.insert(5, (-1, -1))
        coords.insert(7, (1, -1))

    for yc, xc in coords:        
        yn, xn = y+yc, x+xc
        if 0 <= yn < h:
            if 0 <= xn < w:
                if grid[yn][xn] not in blocked:
                    yield (yn, xn)

class Node:
    def __init__(self, data, extra=None):
        self.data = data
        self.connections = {}
        self.extra = extra


    def __repr__(self):
        return f"node {self.data}"

    def add_connection(self, neighbour, weight=0, extra=None):
        if extra:
            self.connections[neighbour.data] = (neighbour, weight, extra)
        else:
            self.connections[neighbour.data] = (neighbour, weight)

    def remove_connection(self, neighbour):
        try:
            del self.connections[neighbour.label]
            print(f"Removed connection between {self} and {neighbour}")
            return True
        except ValueError:
            print(f"Could not remove: did not find {neighbour} in {self}'s connections.")
            return False
        
    def find_path_to(self, target, visits=1, loop_back=False, dfs=True):        
        explore = [{"path":[self], "cost":0}]
        visited = Counter()
        cost = 0


        # while somewhere left to explore and haven't reached target
        while len(explore):
            # next node to explore
            path_data = explore.pop(0)

            path = path_data["path"]
            cost = path_data["cost"]
            
            node = path[-1]
            visited[str(node)] += 1
   
            if node == target:
                if loop_back:
                    loop_back = False
                else:
                    return path, cost
   
            # count neighbours to visit

            found_path = False
            for neighbour, weight in node.connections.values(): 
                if visited[str(neighbour)] < visits or (neighbour == target and len(path) > 2):
                    explore.insert(0 if dfs else -1, {"path":path + [neighbour], "cost":cost+weight})
                    found_path = True
        
        return None
            
        
                
            
                

            
            
          
                         


def get_or_make_node(key, graph, extra=None):
    node = graph.get(key)
    if node is None:
        node = Node(key, extra)
        graph[key] = node
    return node

def alphanum_only(data):
    return "".join(d for d in data if d.isalpha() or d.isdigit())

def create_graph(data, sep_node, sep_conns, weight_format=None, undirectional=True):
    ## TO DO, implement weighted graphs later
    
    graph = {}
    
    for row in data:
        root, conns = row.split(sep_node)
        conns = conns.split(sep_conns)

        node = get_or_make_node(alphanum_only(root), graph)
        for c in conns:
            weight = None
            if weight_format:
                weight = search(weight_format, c).group()
            
            neighbour = get_or_make_node(alphanum_only(c), graph)
            node.add_connection(neighbour)
            if undirectional:
                neighbour.add_connection(node)

    return graph



def calculate_polygon_area(points):
    # specify a named ellipsoid
    geod = Geod(ellps="WGS84")

    pts_str = ", ".join([f"{x} {y}" for x, y in points])

    poly = wkt.loads(f'''\
    POLYGON (({pts_str}))''')

    area = abs(geod.geometry_area_perimeter(poly)[0])

    print('# Geodesic area: {:.3f} m^2'.format(area))
    return poly.area

class PuzzleHelper:

    def __init__(self, day, test_delim, file_delim, debug, pp_args):
        self.day = day
        self.test_delim = test_delim
        self.file_delim = file_delim
        self.debug = debug
        self.pp_args = pp_args
    def bugprint(self, *s, end="\n"):
        if self.debug:
            for item in s:
                print(str(item), end=" ")
            print(end=end)


    def buginput(self, s=""):
        if self.debug:
            print(s)
            input()


    def load_puzzle(self):
        with open(f"day{self.day}.txt") as f:
            data = f.read().replace("\\", "$")

        return data

    def pre_process(self, data, rotate=False, cast_int=True):


        if rotate:  print("Rotating data")
        data = [d for d in data.split(self.file_delim)]
        
        if rotate:
            cols = len(data[0])
            new = [""] * cols
            
            for row in data:
                for i in range(cols):
                    new[i] += row[i]

            data = new

        if not cast_int:
            return data
        
        numeric = all(d.isdigit() for d in data)
        
        if numeric:
            data = list(map(int, data))
        return data


    def check(self, tests, solve):

        success = True

        for row in tests.split(self.test_delim):
            if not len(row):    continue

            data, expected = row.split("///")
            data = self.pre_process(data, *self.pp_args)
            print(data, "should get", expected)
            
            outcome = solve(data)
            if str(outcome).strip() == expected.strip():
                print("Test passed")
            else:
                print("Test failed")
                success = False                
                print(outcome)
                raise Exception("failed the test data")

        return success

    def convert_arg(self, data):
        if set(data) == set(["█", "."]):
            data = data.replace(".", "0").replace("█", "1")
            data = int(data, 2)

        try:
            return int(data)                              # return integer value
        except ValueError:
            if data in "TrueFalseNone": return eval(data) # return bool/null flag
            return data                                   # return > / < string
        
    def process_test_args(self, data):

        data = tuple(map(self.convert_arg, data.split(",")))

        if len(data) == 1:  data = data[0]

        return data

        
            
    
   
               
    def module_tests(self, solution_funcs):


        try:
            with open(f"day{self.day}.tests", encoding="utf-8") as f:
                test_data = f.read()
        except FileNotFoundError:
            print("No module tests found")
            return

        if not input("Run module tests?"):
            return           
        

        test_num = 1
        func = None
        data = {}
        this_test = ""

        print(f"processing {test_data.count('test:')}")
        for line in test_data.splitlines():


            if "test:" in line:
                print(line)
                e = None
                if func:
                    
                    data = {arg:self.process_test_args(value) for arg, value in data.items()}
                    expected = data.pop("result")

                    print(data)

                    

                    

                    actual = eval(f"{func}(**data)", solution_funcs | locals())
         
                    if expected != actual:
                        print(this_test)
                        print(f"RECEIVED: {actual}\n EXPECTED {expected}")
                        print(f"received")
                        debinarise(actual)
                        raise Exception(f"Test number {test_num} failed\n{e}")
                    print(f"Test number {test_num} ({func}) PASSED 🎉")
                    test_num += 1

                    print()
                    
                    
                func = line.split("test:")[1]
                data = {}
                this_test = line + "\n"

            else:
                if ":" in line:
                    line_split = line.split(":")
                    this_arg = line_split[0]
                    if len(line) > 1:
                        data[this_arg] = line_split[1] # test value on same line
                else:
                    data[this_arg] += line

                this_test += line + "\n"

        input("all module tests passed")



if __name__ == "__main__":

    grid = '''
####
#..#
#..#
####'''.strip().splitlines()
    neighbours = tuple(get_neighbours(grid, 1, 1))
    print(neighbours)
    assert neighbours == ((2,1), (1,2))