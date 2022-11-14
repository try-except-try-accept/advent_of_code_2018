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

class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.previous = None
    def __repr__(self):
        return str(self.value)

class Circle:

    def __init__(self, first):
        self.head = Node(first)
        self.head.next = self.head
        self.head.previous = self.head
        self.len = 1
        self.current = self.head

    def place(self, new):
        if new % 23 == 0:
            for j in range(7):                          # go back seven nodes
                self.current = self.current.previous
            
            prev = self.current.previous
            next_ = self.current.next


            next_.previous = prev
            prev.next = next_
            
            removed = self.current.value

            self.current = next_           # re-establish the current node
            return new + removed

        new_node = Node(new)
        self.current = self.current.next

        prev_next = self.current.next

        self.current.next = new_node
        new_node.previous = self.current

        new_node.next = prev_next
        prev_next.previous = new_node
        
        self.current = new_node

        return 0

    def __repr__(self):
        n = self.head
        orig = id(n)
        ref = orig
        out = ""
        
        while True:
       
            out += str(n.value) + " "
            
            n = n.next
            ref = id(n)
            if ref == orig:
                break
        return out


def solve(data):

    data = data[0].split()
    num_players = int(data[0])
    scores = [0 for i in range(num_players)]
    last_marble = int(data[6]) * MULTIPLIER
    current_player = 0
    marble = 1
    circle = Circle(0)

    while marble <= last_marble:
        
        scores[current_player] += circle.place(marble)
        #print(f"[{current_player+1}]  {circle}")
        current_player = (current_player + 1) % num_players
        marble += 1
        
    return max(scores)


MULTIPLIER = 1
if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        MULTIPLIER = 100
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
