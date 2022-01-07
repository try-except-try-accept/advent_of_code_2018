from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 5
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """dabAcCaCBAcCcaDA///10"""

DEBUG = False


def get_next_poly(seq):

    for i, u in enumerate(seq[:-1]):
        n = seq[i+1]
        if abs(ord(n)-ord(u)) == 32:
            return u+n

    return None


def solve(data):
    if type(data) == list:
        data = "".join(data)

    p.bugprint(data)
        
    count = 0

    while True:

        next_poly = get_next_poly(data)
    
        if next_poly is None:
            return len(data)
        else:
            data = data.replace(next_poly, "")

        
        


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
