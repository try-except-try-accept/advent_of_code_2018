from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 11
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """42///(21, 61)
---
18///(33, 45)"""

DEBUG = True

def get_power_level(x, y, serial_num):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_num
    power_level = power_level * rack_id
    power_level = (power_level % 1000) // 100
    return power_level - 5
  


def solve(data):
    count = 0

    cache = {}

    serial_num = int(data[0])

    biggest = [0, 0]
    
    for y in range(297):
        
        for x in range(297):
            tot = 0
            for yc in range(3):
                for xc in range(3):
                    key = (x+xc, y+yc)
                    try:
                        power = cache[key]
                    except KeyError:
                        power = get_power_level(*key, serial_num)
                        cache[key] = power
                    tot += power

            if tot > biggest[0]:
                biggest[0] = tot
                biggest[1] = (x, y)
                print("new biggest", biggest)
            
            
        

        
    

    return str(biggest[1])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = ["8444"]
        #puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
