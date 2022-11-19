from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import inf as INF

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
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######///39514
---
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######///27755
---
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######///28944
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


grid = []
units = []
dead_units = []
graph = {}


def calculate_distance(here, to_here):
    return abs(to_here[0] - here[0]) + abs(to_here[1] - here[1])



def get_optimum_target(targets):
    if not len(targets):
        raise Exception("no targets")
    
    targets = sorted(targets, key=lambda t: t.hp)

    lowest_hp = targets[0].hp


    if DEBUG:
        print("\nORDERED BY hp")
        for t in targets:
            print(t.x, t.y, t.hp)


    return reading_order_sort(list(filter(lambda t: t.hp == lowest_hp, targets)))[0]


def reading_order_sort(coords):

    return sorted(sorted(coords), key=lambda x: x[1])

    


def get_valid_neighbours(x, y, allow_units = False):
    w, h = len(grid[0]), len(grid)
    n = []
    for xc, yc in URLD:
        x2 = x + xc
        y2 = y + yc
        if 0 < x2 < w:
            if 0 < y2 < h:                
                if grid[y2][x2] != "#" and (allow_units or (not any(u.get_pos() == (x2, y2) for u in units))):
                    n.append((x2, y2))

    return reading_order_sort(n)

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


class GNode:

    def __init__(self, location):
        self.location = location
        self.neighbours = set()

    def add(self, neighbour):
        self.neighbours.add(neighbour)
          




    
def bfs(x, y, end):

    q = []
    explored = [(x, y)]
    q.append(Node((x, y), None))
    shortest_path = []
    success = False
    distance = 1
    while q:
        v = q.pop(0)
        if v.loc == end:            
            success = True
            break
        for n in get_valid_neighbours(*v.loc):
            if n not in explored:
                explored.append(n)
                q.append(Node(n, v))
                

    if success:
        path = []
        while v is not None:
            path.append(v.loc)
            v = v.came_from

        return list(reversed(path))
    else:
        return []


    
def find_shortest_path(x, y, end):
    
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

    #if DEBUG:   input()


class Unit:

    def __repr__(self):
        return f"The {self.type} at ({self.x} {self.y})"

    def __init__(self, x, y, t):

        self.type = t
        self.x = x
        self.y = y
        self.hp = 200
        self.ap = 3

    def get_pos(self):
        return (self.x, self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise Exception("Unit type can only be subscripted at [0] or [1]")

    def is_enemy(self, other):
        if self.type == "." or other.type == ".":
            return False
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
        
        targets = self.get_attack_targets()
        dead = None
        if targets:
            if DEBUG:
                print(f"{self.type} at {self.x} {self.y} attack ", end="")
            #Otherwise, the adjacent target with the fewest hit points is selected; in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.
            this_target = get_optimum_target(targets)
            this_target.hp -= self.ap
            if DEBUG:
                print(f"{this_target.type} at {this_target.x} {this_target.y}, reducing hp by {self.ap} to {this_target.hp}")
            if this_target.hp <= 0:
                if DEBUG:
                    print(this_target.type, "Died")
                
                this_target.type = "."
                dead =  this_target

            if DEBUG:
                display_grid()

            return dead
                
    def get_attack_targets(self):
        other_units = [u for u in units if u.is_enemy(self)]
        
        # do i already have a target?
        targets_already = [o for o in other_units if o.get_pos() in get_valid_neighbours(self.x, self.y, allow_units=True) and o.hp > 0]

        if targets_already:
##            print("Target already", targets_already)
            return targets_already
        else:
            
            return None

    def locate_direction(self):

        
        
        other_units = [u for u in units if u.is_enemy(self)]
        
        # do i already have a target?
        already = self.get_attack_targets()
        if already:
            if DEBUG:
                print(f"{self} already has a target. No move required.")
                display_grid()
                
            return None, False
        
        in_range = set()

        for u in other_units:
            for n in get_valid_neighbours(u.x, u.y):
                in_range.add(n)

        if DEBUG:
            print("in range")        
            display_grid(mark=in_range, symbol='?')

        
               
        reachable = [i for i in in_range if len(bfs(self.x, self.y, i)) > 1]

        if DEBUG:
            
            for i in in_range:
                path = bfs(self.x, self.y, i)
                if len(path) > 1:
                    
                    print(f"Found a path to {i} from {self.x} {self.y}")
                    print(path)
                    display_grid(mark=path, symbol="*")

        if DEBUG:
            if len(reachable):
                print("reachable")
                display_grid(mark=reachable, symbol='@')
                

        try:
            closest_distance = min(calculate_distance(self.get_pos(), other) for other in reachable)
        except ValueError: #no reachable target
            if DEBUG:
                print("Nothing is reachable")
            return None, False
        
        nearest = [i for i in reachable if calculate_distance(self.get_pos(), i) == closest_distance]
        if DEBUG:
            print("nearest")
            display_grid(mark=nearest, symbol='!')

        target = min(nearest, key=lambda x: x[1])
        if DEBUG:            
            print(f"{self} has chosen to move  towards {target}")
            display_grid(mark=[target], symbol='+')

        return target, True

    def move(self, target):
        path = find_shortest_path(self.x, self.y, target)
        if DEBUG:
            print(path)

        

        try:
            if DEBUG:
                print(f"{self} moved to ", end="")
            self.x, self.y = path[1]
            if DEBUG:
                print(f"({self.x}, {self.y})")
            
        except IndexError:
            if DEBUG:
                print("NO PATH AVAILABLE!")
            return False


def all_dead(units):
    type_ = units[0].type
    tot = units[0].hp


    for u in units[1:]:
        
        if u.type != "." and u.type != type_:
            break
    else:
        return True
    return False


test_no = 1

def construct_graph(units):

    graph = {}
  
    for y, row in enumerate(data):
        grid_row = []
        for x, cell in enumerate(row):

            if any(unit.get_pos() == (x, y) for unit in units):
                continue
            
            this_node = graph.get((x, y))
            if this_node is None:
                this_node = GNode(x, y)
                graph[(x, y)] = this_node

            for (nx, yx) in get_valid_neighbours(x, y, allow_units=True):
                neighbour_node = graph.get((x, y))
                if neighbour_node is None:
                    neighbour_node = GNode(x, y)
                    graph[(x, y)] = neighbour_node
                this_node.add(neighbour_node)


def solve(data):

    global grid, units, DEBUG, dead_units, test_no, graph
    grid, units, dead_units = [], [], []
    #DEBUG = True
    debug2 = False

    #DEBUG = True

    if data[0][0] == "d":
        data[0] = data[0][1:]
        debug2 = True





    for y, row in enumerate(data):
        grid_row = []
        for x, cell in enumerate(row):
            if cell in "GE":
                units.append(Unit(x, y, cell))
                cell = "."
                
            grid_row.append(cell)

        grid.append(grid_row)

    print(f" test no {test_no} ")
    test_no += 1
    display_grid()
    input()

    next_round = 1
   
    r = 0
    while True:
        
        print("**************")
        print("Round", r)
        print("**************")
        if DEBUG and r == next_round:   next_round = int(input("next round? "))

        last = units[-1]
        
        for u in units:

 
            if DEBUG:
                print("Handling move for", str(u))

            if u.type == ".":
                continue
      
            
            towards, move_needed = u.locate_direction()
            if move_needed and u.type != ".":
                u.move(towards)



            if u.type != ".":
                u.perform_attack()

            adjust = 1 if u == last else 0 # dodgy
            

            if all_dead(units):
                display_grid()
                hp_left = sum(u.hp for u in units if u.type != ".")

                print(r, "x", hp_left)
                return (r + adjust) * hp_left
        
            
            
        units = sorted(u for u in units if u.type != ".")


            
        r += 1
            
        


        
        


if __name__ == "__main__":
  
    
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if True: #p.check(TESTS, solve):
        grid, units, dead_units, graph = [], [], [], {}
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

