from re import search, match, findall
from collections import Counter


GREEDY = "\[.+\]" # greedily match anything between [ and ]
LAZY = "\[.+?\]"  # lazily match anything between [ and ]

class PuzzleHelper:

    def __init__(self, day, test_delim, file_delim, debug, pp_args):
        self.day = day
        self.test_delim = test_delim
        self.file_delim = file_delim
        self.debug = debug
        self.pp_args = pp_args

    def bugprint(self, *s, end="\n"):
        if self.debug:
            for item in s:
                print(str(item), end=" ")
            print(end)


    def buginput(self, s=""):
        if self.debug:
            print(s)
            input()


    def load_puzzle(self):
        with open(f"day{self.day}.txt") as f:
            data = f.read().strip()

        return data

    def pre_process(self, data, rotate=False, cast_int=True):


        if rotate:  print("Rotating data")
        data = [d for d in data.split(self.file_delim) if d.strip()]
        
        if rotate:
            cols = len(data[0])
            new = [""] * cols
            
            for row in data:
                for i in range(cols):
                    new[i] += row[i]

            data = new

        if not cast_int:
            return data
        
        numeric = all(d.isdigit() for d in data)
        
        if numeric:
            data = list(map(int, data))
        return data


    def check(self, tests, solve):

        success = True

        for row in tests.split(self.test_delim):
            if not len(row):    continue

            data, expected = row.split("///")
            data = self.pre_process(data, *self.pp_args)
            print(data, "should get", expected)
            
            outcome = solve(data)
            if str(outcome).strip() == expected.strip():
                print("Test passed")
            else:
                print("Test failed")
                success = False                
                print(outcome)
                raise Exception("failed the test data")

        return success

