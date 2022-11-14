from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2///138
"""

DEBUG = True

class Node:
    def __init__(self, num_children, num_meta, alias):

        self.children_to_come = num_children
        self.meta_to_come = num_meta
        self.children = []
        self.meta = []
        self.alias = chr(alias)
        

    def add_child(self, new):
        #print(f"add {new.alias} as child of {self.alias}")
        
        if self.children_to_come == 0:
            raise Exception("Too many children")
        else:
            self.children_to_come -= 1
            #print(f"{self.alias} has {self.children_to_come} children left")
            self.children.append(new)
    

    def add_meta(self, new):
        if self.meta_to_come == 0:
            raise Exception("Too many meta")
        else:
            self.meta_to_come -= 1
            #print(f"{self.alias} has {self.meta_to_come} meta left")
            self.meta.append(new)

    def child_msg(self):
        pass
        #print(f"{self.alias} {self.children_to_come} to come")

def traverse(n, count=0):
    count += sum(n.meta)
    for node in n.children:
       count = traverse(node, count)

    return count

def solve(data):
    # 0 defining node
    # 1 parsing meta
    state = 0        
    nums = list(map(int, data[0].split()))

    root = None

    alias = 65

    node_stack = []
    first = True
    while nums:
        while first or node_stack[-1].children_to_come > 0:
            
            num_children, num_meta = nums.pop(0), nums.pop(0)
            node_stack.append(Node(num_children, num_meta, alias))
            alias += 1
            if root:
                parent.add_child(node_stack[-1])

            else:
                root = node_stack[-1]
            parent = node_stack[-1]

            
            first = False
            node_stack[-1].child_msg()

        
        

            
        for i in range(node_stack[-1].meta_to_come):

            node_stack[-1].add_meta(nums.pop(0))

        node_stack.pop(-1)
        if node_stack:
            parent = node_stack[-1]
        
    count = traverse(root)
        

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
