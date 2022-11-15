from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 12
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #///325"""

DEBUG = True

last_tot = 0
diff_q = []


def solve(data):
    plants = "..." + data[0].replace("initial state: ", "") + "..........."
    rules = {rule.split(" => ")[0]:rule.split(" => ")[1] for rule in data[1:]}

    global last_tot
    
    last = plants

    for generation in range(0, LIMIT):
        #print(f"{str(generation).zfill(2)}: {plants}")


        
        new_plants = list("." * len(plants))

        for i in range(0, len(plants)-5):

            
            low = max([i-2, 0])
            buffer = ""
            if low == 0:
                buffer = abs(i-2) * "."
            
            
            key = buffer + plants[low:i+3]
            plant = rules.get(key)

            if plant:
                new_plants[i] = plant
            

        plants = "".join(new_plants) + "."
        


    
        pots_w_plants = sum([i-3 for i in range(len(plants)) if plants[i] == "#"])



        diff_q.append(pots_w_plants - last_tot)
        print(diff_q)

        if len(diff_q) > 2 and diff_q[-1] == diff_q[-2]:            

            return pots_w_plants + ((LIMIT - generation-1) * diff_q[-1])

        last_tot = pots_w_plants
        

        
        
    return sum(pots_w_plants)
    

    

LIMIT = 20


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    

    if True:
        LIMIT = 50000000000
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
