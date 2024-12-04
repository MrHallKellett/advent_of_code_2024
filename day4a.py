from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 4
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX///18"""



DEBUG = True

class List(list):
    def __getitem__(self, key):
        
        if key < 0:
            raise IndexError
        else:
            return super().__getitem__(key)



def solve(data):
    count = 0

    W = len(data[0])
    H = len(data)
    def check(x, y):
        return True


    ########################################
    
    def left(d, x, y):

        
        return all([d[y][x] == "X",
        d[y][x-1] == "M",
        d[y][x-2] == "A",
        d[y][x-3] == "S"])
        

    ########################################
    
    def right(d, x, y):

        return all([d[y][x] == "X",
        d[y][x+1] == "M",
        d[y][x+2] == "A",
        d[y][x+3] == "S"])


    ########################################
    
    def up(d, x, y):



        return all([d[y][x] == "X",
        d[y-1][x] == "M",
        d[y-2][x] == "A",
        d[y-3][x] == "S"])

    ########################################
        
    def down(d, x, y):

        
        return all([d[y][x] == "X",
        d[y+1][x] == "M",
        d[y+2][x] == "A",
        d[y+3][x] == "S"])

    ########################################
        
    def diag1(d, x, y):

        return all([d[y][x] == "X",
        d[y+1][x+1] == "M",
        d[y+2][x+2] == "A",
        d[y+3][x+3] == "S"])

    ########################################
        
    def diag2(d, x, y):

        
        return all([d[y][x] == "X",
        d[y+1][x-1] == "M",
        d[y+2][x-2] == "A",
        d[y+3][x-3] == "S"])

    ########################################
        
    def diag3(d, x, y):

        
        return all([d[y][x] == "X",
        d[y-1][x+1] == "M",
        d[y-2][x+2] == "A",
        d[y-3][x+3] == "S"])

    ########################################
        
    def diag4(d, x, y):
   
        return all([d[y][x] == "X",
        d[y-1][x-1] == "M",
        d[y-2][x-2] == "A",
        d[y-3][x-3] == "S"])
    

    funcs = [diag1,diag2,diag3,diag4,left,right,up,down]

    data = List(List(row) for row in data)

    for y in range(H):
        for x in range(W):
            for fun in funcs:
                try:
                    if fun(data, x, y):
                        count += 1
                except IndexError:
                    pass

   

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
