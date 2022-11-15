from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>///3"""

DEBUG = True

class Light:
    def __init__(self, position=None, velocity=None):        
        self.pos = position
        self.vel = velocity        
        
    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        


def display(lights, top_y, bot_y):    

    left_x = min(light.pos[0] for light in lights)
    rite_x = max(light.pos[0] for light in lights)
    
    for y in range(top_y, bot_y):
        line = ""
        for x in range(left_x, rite_x):
            cell = "."
            for light in lights:
                if light.pos == [x, y]:
                    cell = "#"
                    break
            line += cell
        print(line)
    print() 

def solve(data):

    lights = []

    for row in data:
        row = row.replace("<", "[").replace(">", "]").replace(" vel", ", vel")        
        lights.append(eval(f"Light({row})"))

    second = 0
    while True:
        for light in lights:
            light.move()

        second += 1

        first = light.pos[1]


        top_y = min(light.pos[1] for light in lights)
        bot_y = max(light.pos[1] for light in lights) + 1



        if abs(bot_y - top_y) < 50:
            display(lights, top_y, bot_y)
        
        if bot_y == top_y + 8:            
            return second
            






if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
