from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """59414///2018"""

DEBUG = True


class Recipe:
    def __init__(self, value):
        self.value = int(value)
        self.next = None

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other.value

class Recipes:
    def __init__(self, sequence):

        self.elf1 = Recipe(3)
        self.elf2 = Recipe(7)
        self.elf1.next = self.elf2
        self.elf2.next = self.elf1
        self.head = self.elf1
        self.tail = self.elf2
        self.length = 2
        self.last5 = [3, 7]
        self.sequence = list(map(int, sequence))

    def new(self):
        for digit in str(self.elf1 + self.elf2):
            digit = int(digit)
            self.head = self.tail.next                  # remember the head
            new_recipe = Recipe(digit)                  # make new
            self.tail.next = new_recipe                 # tail links to new
            self.tail = new_recipe                      # the tail is now the new
            new_recipe.next = self.head                 # the new links back to the head
            self.length += 1

            self.last5.append(digit)
            if len(self.last5) > len(self.sequence):
                self.last5.pop(0)

            #print("Comparing", self.last5, self.sequence)
            if self.last5 == self.sequence:
                return self.length - len(self.sequence)

        movement =  self.elf1.value + 1

        #print(f"{self.elf1} will move {movement} times")

        for i in range(movement):
            self.elf1 = self.elf1.next

        movement = self.elf2.value + 1
        
        for i in range(movement):
            self.elf2 = self.elf2.next

    def display(self):
        n = self.head
        while True:
            if n == self.elf1:
                display = f"({n.value})"
            elif n == self.elf2:
                display = f"[{n.value}]"
            else:
                display = str(n) + "  "
            print(display, end=" ")
            n = n.next
            if n == self.head:
                break


        print()
            


def solve(data):

    elf1 = 0
    elf2 = 1

    sequence = list(map(int, data[0]))
    print(sequence, "is the sequence")

    r = Recipes(sequence)
    
    while True:

        result = r.new()
        if result:
            return result

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
