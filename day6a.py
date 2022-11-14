from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 6
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9///17
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

    aliases = {p:chr(128512+i) for i, p in enumerate(points)}
    
    areas = Counter({aliases[p]:1 for p in points})
    grid = [[" " for x in range(max_width)] for y in range(max_height)]
    for y in range(max_height):
        for x in range(max_width):
            cell = aliases.get((x, y))
            if cell is None:
                distances = [(manhattan(*p, x, y),p) for p in points]
                distances = [d for d in distances if d[0] == min(distances)[0]]
                if len(distances) == 1:                    
                    closest = distances[0][1]
                    areas[aliases[closest]] += 1
                    cell = aliases[closest].lower()                              
                else:
                    cell = "."
            
            grid[y][x] = cell

    dump("before", grid)

    # remove any area touching perimeter
    for k in "".join(grid[0] + grid[-1]) + "".join(row[0]+row[-1] for row in grid):        
        if k.upper() in areas:
            areas.pop(k.upper())
            grid = [[i if i!=k else " " for i in row] for row in grid]

    dump("after", grid)  

    return areas.most_common()[0][1]



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
