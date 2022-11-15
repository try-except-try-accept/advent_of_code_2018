from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy

PP_ARGS = False, False #rotate, cast int

DAY = 13
TEST_DELIM = "***"
FILE_DELIM = "\n"
TESTS = """/>-<\\ 
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
///(6, 4)"""

DEBUG = True


DIRECTIONS = ["left", "straight", "right"]
ORIENTATIONS = "<v>^"
TRACK_PIECES = "-|-|"
MOVE_VECTORS = ((-1, 0),
                (0, 1),
                (1, 0),
                (0, -1))

class Car:
    def __init__(self, orientation, x, y):
        self.orientation = orientation
        self.x = x
        self.y = y
        self.pointer = 0
        self.history = []

    def reorient(self, d=None):
        prev = ORIENTATIONS[self.orientation]
        
        if d == "left":
            self.orientation = [1, 0, 3, 2][self.orientation]
        elif d == "right":
            self.orientation = [3, 2, 1, 0][self.orientation]
        else:
            d = DIRECTIONS[self.pointer]
            change = 0
            if d == "left":
                change = 1
            elif d == "right":
                change = -1
            self.orientation = (self.orientation + change) % len(ORIENTATIONS)
            self.pointer = (self.pointer + 1) % len(DIRECTIONS)
        self.history.append(f"Changed from {prev} to {ORIENTATIONS[self.orientation]}")

    def __lt__(self, other):
        if self.y > other.y:
            return True
        elif self.y == other.y:
            if self.x > other.x:
                return True
        return False

    def __repr__(self):
        return ORIENTATIONS[self.orientation]

    def get_pos(self):
        return (self.x, self.y)

    def move(self, cars, track, debug = False):
        
        v = MOVE_VECTORS[self.orientation]
    
        # < v > ^
        # 0 1 2 3

        self.x += v[0]
        self.y += v[1]
    
        x, y = self.x, self.y
        this_track = track[y][x]

        self.track = this_track

        self.history.append(f"encountered {this_track}")


        if this_track == " ": # debug error

            while True:
                d = self.history.pop(0)
                print(d)
                input()
            raise Exception("Car went off the track...")

        if this_track == "/":
            self.reorient("left")
        elif this_track == "\\":
            self.reorient("right")       
        elif this_track == "+": # intersection
            self.reorient()


        if debug:
            this_grid = ""

            for y in range(self.y - 50, self.y + 50):
                for x in range(self.x -50, self.x + 50):
                    try:
                        for car in cars:
                            if car.get_pos() == (x, y):
                                this_grid += str(car)
                            else:
                                this_grid += track[y][x]
                    except IndexError:
                        pass
                this_grid += "\n"

            self.history.append(this_grid)

        


        
def display(track, cars):

    for y, row in enumerate(track):
        for x, cell in enumerate(row):
            for car in cars:
                if car.x == x and car.y == y:
                    cell = car
            print(cell, end="")
        print()

def solve(data):
    count = 0

    track = [[]]
    cars = []

    last_ten = []

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell in ORIENTATIONS:
                cell = ORIENTATIONS.index(cell)
                cars.append(Car(cell, x, y))
                cell = TRACK_PIECES[cell]
            track[-1].append(cell)
        track.append([])

    tick = 0
    tick_history = []
    last_found = False
    while not last_found:
        tick += 1

        cars = sorted(cars)
        new_cars = None
        
        for car in cars:
            if new_cars and car not in new_cars:
                continue
            
            car.move(cars, track)
      
            car_positions = Counter(car.get_pos() for car in cars)

            most_common_loc = car_positions.most_common()[0]
            if most_common_loc[1] >= 2:
                crash = most_common_loc[0]
                
                new_cars = [car for car in cars if car.get_pos() != crash]
                
                cars = new_cars
                print(len(cars), "left")


        tick_history.append(", ".join([f"{car} at {car.get_pos()} (on {car.track})" for car in cars]))
  

        if len(cars) == 1:
            last_found = True


    return cars[0].get_pos()
                





if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
