from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 15
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######///27730
---
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######///36334
---
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########///18740"""

URLD = ((0, -1),
        (1, 0),
        (-1, 0),
        (0, 1))

DEBUG = False

def calculate_distance(here, to_here):
    return abs(to_here[0] - here[0]) + abs(to_here[1] - here[1])


grid = []
units = []
dead_units = []


def get_valid_neighbours(x, y, allow_units = False):
    w, h = len(grid[0]), len(grid)
    for xc, yc in URLD:
        x2 = x + xc
        y2 = y + yc
        if 0 < x2 < w:
            if 0 < y2 < h:                
                if grid[y2][x2] != "#" and (allow_units or (not any(u.get_pos() == (x2, y2) for u in units))):
                    yield (x2, y2)

def bfs(x, y, end, this_path=None, paths=None, d=0):
    if this_path is None:
        paths = set()
        this_path = ""

    if (x, y) == end:
        if this_path not in paths:

            paths.add(this_path)
        return paths
   
    neighbours = list(get_valid_neighbours(x, y))
    old_path = this_path
    for nx, ny in neighbours:
        if f"{nx},{ny}" in this_path:
            continue
        new_path = old_path + f"{nx},{ny}|"
        paths = bfs(nx, ny, end, new_path, paths, d+1)
        
    return paths

class Node:
    def __init__(self, location, came_from):
        self.loc = location
        self.came_from = came_from

def bfs(x, y, end):

    q = []
    explored = [(x, y)]
    q.append(Node((x, y), None))
    shortest_path = []
    while q:
        v = q.pop(0)
        if v.loc == end:
            #print(explored)
            break
        for n in sorted(get_valid_neighbours(*v.loc), key=lambda x: x[1]):
            if n not in explored:
                explored.append(n)
                q.append(Node(n, v))

            
    path = []
    while v is not None:
        path.append(v.loc)
        v = v.came_from

    return list(reversed(path))

def find_shortest_path(x, y, end):
    print("get from" , x, y, "to" ,end)
    return bfs(x, y, end)

    # old implementation - wrong - dfs?
    shortest = min(bfs(x, y, end), key=len)
    shortest = shortest[:-1].split("|")
    
    return [tuple(map(int, t.split(","))) for t in shortest]


def display_grid(mark=(), symbol="", hp_mode=False):
    hp = ""

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            for u in units:
                if u.x == x and u.y == y:
                    cell = u.type
                    hp +=  f"{cell} ({u.hp}), "
                    break

            if (x, y) in mark:
                cell = symbol

            print(cell, end="")
        print("  ",hp)
        hp = ""

    if DEBUG:   input()


class Unit:

    def __repr__(self):
        return f"{self.type} {self.x} {self.y}"

    def __init__(self, x, y, t):

        self.type = t
        self.x = x
        self.y = y
        self.hp = 200
        self.ap = 3

    def get_pos(self):
        return (self.x, self.y)

    def is_enemy(self, other):
        return self.type != other.type

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y == other.y:
            if self.x < other.x:
                return True
        return False

    def perform_attack(self):
        global DEBUG, dead_units, units
        if DEBUG:
            print(f"{self.type} at {self.x} {self.y} attack ", end="")
        targets = self.get_attack_targets()

        if targets:
            #Otherwise, the adjacent target with the fewest hit points is selected; in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.
            this_target = min(targets, key=lambda x: x.hp)
            this_target.hp -= self.ap
            if DEBUG:
                print(f"{this_target.type} at {this_target.x} {this_target.y}, reducing hp by {self.ap} to {this_target.hp}")
            if this_target.hp <= 0:
                print(this_target.type, "Died")
                
                this_target.type = "."
                return this_target
                #units.remove(this_target)
                
    def get_attack_targets(self):
        other_units = [u for u in units if u.is_enemy(self)]
        
        # do i already have a target?
        targets_already = [o for o in other_units if o.get_pos() in get_valid_neighbours(self.x, self.y, allow_units=True)]

        if targets_already:
##            print("Target already", targets_already)
            return targets_already
        else:
            if DEBUG:
                print(self.x, self.y, "no targets")
            return None

    def locate_direction(self):

        
        
        other_units = [u for u in units if u.is_enemy(self)]
        
        # do i already have a target?
        already = self.get_attack_targets()
        if already:
            return None, False
        
        in_range = []

        for u in other_units:
            in_range += list(get_valid_neighbours(u.x, u.y))

        if DEBUG:
            print("in range")        
            display_grid(mark=in_range, symbol='?')

        # find reachable
        reachable = [i for i in in_range if len(bfs(self.x, self.y, i)) > 0]        

        if DEBUG:    
            display_grid(mark=reachable, symbol='@')
        
        # find nearest
        try:
            closest_distance = min(calculate_distance(self.get_pos(), other) for other in reachable)
        except ValueError: #no reachable target
            return None, False
        
        nearest = [i for i in reachable if calculate_distance(self.get_pos(), i) == closest_distance]
        if DEBUG:
            print("nearest")
            display_grid(mark=nearest, symbol='!')
##
        # select first
        target = min(nearest, key=lambda x: x[1])
        if DEBUG:
            print(nearest)
            print("chosen")
            display_grid(mark=[target], symbol='+')

        return target, True

    def move(self, target):
        path = find_shortest_path(self.x, self.y, target)
        print(path)
##        print("Shortest path?")
##        display_grid(path, "*")
        try:
            self.x, self.y = path[1]
        except IndexError:
            return False
##
##        print("moved")
##        display_grid()

        
def solve(data):

    global grid, units, DEBUG, dead_units
    grid, units, dead_units = [], [], []


    for y, row in enumerate(data):
        grid_row = []
        for x, cell in enumerate(row):
            if cell in "GE":
                units.append(Unit(x, y, cell))
                cell = "."
            grid_row.append(cell)

        grid.append(grid_row)


    display_grid()
    
    
    r = 1
    while True:
        print("Round", r)
        for u in units:
   
            if DEBUG:
                print("Handling move for", str(u))
      
            
            towards, move_needed = u.locate_direction()
            if move_needed:
                u.move(towards)

            if DEBUG:
                print("moved")
                display_grid()


            dead_units.append(u.perform_attack())
            if DEBUG:
                print("attack")
                display_grid(hp_mode = True)

            
            
        units = sorted(u for u in units if u.type != ".")

        dead_units = []
            

        
        type_ = units[0].type
        tot = units[0].hp
        print("tot is", tot)
        for u in units[1:]:
            print(u.type)
            if u.type != type_:
                break
            else:
                tot += u.hp
        else:
            display_grid()
            print(tot, "*", r)
            return tot * r    


        r += 1


if __name__ == "__main__":
  
    
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        grid, units, dead_units = [], [], []
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

