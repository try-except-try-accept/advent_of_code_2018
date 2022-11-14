from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 6
MAX = 32
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9///16
"""

DEBUG = True
from collections import Counter

def manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def dump(fn, grid):
    with open(f"day6vis_{fn}.txt", "w", encoding="utf-16") as f:
        for row in grid:
            f.write("".join(row)+"\n")



def solve(data):
    points = [tuple(map(int, row.split(","))) for row in data]

    max_width = max(points)[0] + 2
    max_height = max(points, key=lambda x: x[1])[1] + 1

   
    print(max_width, max_height)

    regions = []
    count = 0
    
    grid = [[" " for x in range(max_width)] for y in range(max_height)]
    for y in range(max_height):
        for x in range(max_width):

            count += 1 if sum(manhattan(*p, x, y) for p in points)<MAX else 0
            

    return count
            
            



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        MAX = 10000
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
