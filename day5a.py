from re import search, match, findall
from collections import Counter
from helpers import *

PP_ARGS = False, False #rotate, cast int

DAY = 5
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
*****
75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47///143"""

DEBUG = True


def solve(data):
    count = 0

    rules, updates = "\n".join(data).split("\n*****\n")

    rules = [list(map(int, rule.split("|"))) for rule in rules.splitlines()]

    updates = [list(map(int, up.split(","))) for up in updates.splitlines()]
    
    for update in updates:
        okay = True
        for before, after in rules:
            
            if before in update and after in update and update.index(before) > update.index(after):
                okay = False

        if okay:
            
            count += update[len(update)//2]
            
        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
