from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 9
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """2333133121414131402///2858"""

DEBUG = True
def decompress(data):
    result = []
    for i in range(0, len(data), 2):
        val = i // 2
        result.extend([val for _ in range(data[i])])
        try:
            result.extend([None] * data[i+1])
        except IndexError:
            pass
    return result


def attempt_to_move_chunk(data, chunk, chunk_pos):
    x = len(chunk)
    for i in range(0, chunk_pos):
        if data[i] == None:
            count = 0
            for j in range(i, len(data)):
                if data[j] == None:
                    count += 1  
                    if count == x:
                        for p in range(chunk_pos, chunk_pos + len(chunk)):
                            data[p] = None
                        return True, data[:i] + chunk + data[i+x:]
                else:
                    break
    return False, data

def find_chunk(data):
    prev = None
    chunk = []

    for file_id in sorted([d for d in set(data) if d!=None], reverse=True):

        chunk_found = False
        j = len(data) - 1
        while not chunk_found and j > 0:
            
            this = data[j]

            if this == file_id:
                chunk += [this]

            elif chunk:
                chunk_found = True
                #print(f"Found a chunk {chunk} at pos {j+1}")
                
                success, data = attempt_to_move_chunk(data, chunk, j+1)
                if success:
                    #print("".join(str(i)  if i is not None else "." for i in data))
                    #input(f"moved a chunk {chunk}")
                    pass
                chunk = []

            j -= 1


    return data

def checksum(data):
    return sum([i*j if j is not None else 0 for i, j in enumerate(data)])

def solve(data):
    data = data[0]
    data = list(map(int, list(data)))
    data = decompress(data)
    data = find_chunk(data)
    
    return checksum(data)

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
