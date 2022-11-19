from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 16
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]///1"""

DEBUG = True

def math_op(register, operands, op, immediate=False):
    if not immediate:
        exp = f"{register[operands[0]]} {op} {register[operands[1]]}"
    else:
        exp = f"{register[operands[0]]} {op} {operands[1]}"
        
        
    register[operands[2]] = eval(exp)
    return register

def eq_op(register, operands, op, mode):
    if mode == "ir":
        exp = f"{operands[0]} {op} {register[operands[1]]}"
    elif mode == "ri":
        exp = f"{register[operands[0]]} {op} {operands[1]}"
    else:
        exp = f"{register[operands[0]]} {op} {register[operands[1]]}"
        
    register[operands[2]] = 1 if eval(exp) else 0
    return register



def addr(register, operands):
    return math_op(register, operands, "+", immediate=False)

def addi(register, operands):
    return math_op(register, operands, "+", immediate=True)

def mulr(register, operands):
    return math_op(register, operands, "*", immediate=False)

def muli(register, operands):
    return math_op(register, operands, "*", immediate=True)

def borr(register, operands):
    return math_op(register, operands, "|", immediate=False)

def bori(register, operands):
    return math_op(register, operands, "|", immediate=True)

def banr(register, operands):
    return math_op(register, operands, "&", immediate=False)

def bani(register, operands):
    return math_op(register, operands, "&", immediate=True)

def setr(register, operands):
    register[operands[2]] = register[operands[0]]
    return register

def seti(register, operands):
    register[operands[2]] = operands[0]
    return register

def eqrr(register, operands):
    return eq_op(register, operands, "==", "rr")

def eqir(register, operands):
    return eq_op(register, operands, "==", "ir")

def eqri(register, operands):
    return eq_op(register, operands, "==", "ri")

def gtir(register, operands):
    return eq_op(register, operands, ">", "ir")

def gtri(register, operands):
    return eq_op(register, operands, ">", "ri")
    
def gtrr(register, operands):
    return eq_op(register, operands, ">", "rr")
    





def solve(data):
    count = 0



    while data:
        matches = 0

        before = data.pop(0)
        if "Before" not in before:
            break
        
        instruction = data.pop(0)
        after = data.pop(0)

        

        before = eval(before.replace("Before: ", ""))
        instruction = tuple(map(int, instruction.split(" ")))
        
        after = eval(after.replace("After:  ", ""))


        for op in [addr, addi, mulr, muli, banr, bani, borr, bori,
                   setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]:

            
            
            result = op(list(before), operands)
            

            

            if result == after:
                matches += 1
                

        if matches >= 3:
            count += 1



    return count



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
