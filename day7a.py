from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 7
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.///CABDFE
"""

DEBUG = True


def solve(data):
    pre_reqs = {}
    all_tasks = set()
    has_pre_req = ""
    
    for row in data:
        row = row.split()
        before, after = row[1], row[7]
        if after in pre_reqs:
            pre_reqs[after].append(before)
        else:
            pre_reqs[after] = [before]

        has_pre_req += after

        all_tasks.add(after)
        all_tasks.add(before)
        
    current_tasks = set([i for i in all_tasks if i not in has_pre_req])
    task_limit = len(all_tasks)

    order = ""

    print(pre_reqs)


    while len(order) != task_limit:
        print("Which task next out of", current_tasks)
        this_task = min(current_tasks)    
        order += this_task
        current_tasks.remove(this_task)

        for after, before in pre_reqs.items():
            if this_task in before:
                before.remove(this_task)
                if len(before) == 0:
                    current_tasks.add(after)

    return order




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
