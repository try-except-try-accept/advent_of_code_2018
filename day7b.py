from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 7
TEST_DELIM = "---"
WORKERS = 2
T_DEDUCTION = 60
FILE_DELIM = "\n"
TESTS = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.///15
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

    at_work = [None for i in range(WORKERS)]

    second = 0
    while not(all(a is None for a in at_work)) or len(order) != task_limit:
        while None in at_work and current_tasks:
            this_task = min(current_tasks)
            print("find worker")
            i = at_work.index(None)
            at_work[i] = (this_task, second)
            print(f"Worker {i} assigned task {this_task} at {second}")
            current_tasks.remove(this_task)
            order += this_task

        # check for finished tasks

        for i, task in enumerate(at_work):
            if task is not None:
                task, start_sec = task
                if second - start_sec == ord(task) - T_DEDUCTION - 5:
                    at_work[i] = None
                    print(f"Worker {i} finished task {task} at {second}")

                    for after, before in pre_reqs.items():
                        if task in before:
                            before.remove(task)
                            if len(before) == 0:
                                current_tasks.add(after)
                    
        second += 1
        
        
    print(order)
    input()
    return second




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        WORKERS = 5
        T_DEDUCTION = 0
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
