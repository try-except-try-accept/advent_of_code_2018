from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """9///5158916779"""

DEBUG = True

def display(recipes, elf1, elf2):
    for i in range(len(recipes)):
        if i == elf1:
            print(f"({recipes[i]})", end=" ")
        elif i == elf2:
            print(f"[{recipes[i]}]", end=" ")
        else:
            print(recipes[i], end= "   ")
    print()


def solve(data):

    elf1 = 0
    elf2 = 1

    improve_after = int(data[0])

    recipes = [3,7]

    while len(recipes) != improve_after + 10:

        #display(recipes, elf1, elf2)

        for digit in list(str(recipes[elf1] + recipes[elf2])):
            recipes.append(int(digit))


        elf1 = (elf1 + recipes[elf1] + 1)  % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


    
    return "".join(str(i) for i in recipes[-10:])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
