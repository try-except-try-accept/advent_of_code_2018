from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 9
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """9 players; last marble is worth 25 points///32
---
10 players; last marble is worth 1618 points///8317
---
13 players; last marble is worth 7999 points///146373
---
17 players; last marble is worth 1104 points///2764
---
21 players; last marble is worth 6111 points///54718
---
30 players; last marble is worth 5807 points///37305"""

DEBUG = True

class Circle:

    def __init__(self, first):
        self.marbles = [first]
        self.current = 0
        self.display = []

    def place(self, new):

        if new % 23 == 0:
            self.current -= 7
            if self.current < 0:
                self.current = len(self.marbles) - abs(self.current)

            
            removed = self.marbles.pop(self.current)
            self.display = " ".join(str(i) for i in self.marbles)

            return new + removed

        self.current += 2

        if self.current > len(self.marbles):
            self.current = 1
            
        self.marbles.insert(self.current, new)
        self.display = " ".join(str(i) for i in self.marbles)

        return 0

    def __repr__(self):
        return self.display


def solve(data):

    data = data[0].split()
    num_players = int(data[0])
    scores = [0 for i in range(num_players)]
    last_marble = int(data[6])
    current_player = 0
    marble = 1
    circle = Circle(0)

    while marble <= last_marble:
        
        scores[current_player] += circle.place(marble)
        #print(f"[{current_player+1}]  {circle}")
        current_player = (current_player + 1) % num_players
        marble += 1
        
    return max(scores)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
