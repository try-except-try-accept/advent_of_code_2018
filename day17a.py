from re import search, match, findall
from collections import Counter, defaultdict
from helpers import PuzzleHelper
from math import inf as INF

PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504///57"""

DEBUG = True

CLAY = '#'
SAND = '.'
SPRING = '+'
STILL = "~"
FLOW = "|"
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0
UP = 0, -1
HORIZ = -1, 1, 0
SYM_MAP = {DOWN:'v', LEFT:'<', RIGHT:'>', UP:'^'}
WATER = SYM_MAP.values()

grid = []

buckets = None

def render(data):
    global buckets
    
    buckets = {}

    x_max = 0
    y_max = 0
    x_min = INF
    y_min = 0

    clay_coords = set()

    for row in data:

        x, y = row.split(", ")
        if x[0] == 'y':
            x, y = y, x

        x = tuple(map(int, x.replace("x=", "").split("..")))
        y = tuple(map(int, y.replace("y=", "").split("..")))

        ref = None
        if len(x) == 1:
            x_start, x_end = x[0], x[0]
        else:
            x_start, x_end = x[0], x[1]
        if len(y) == 1:
            ref = y
            y_start, y_end = y[0], y[0]
        else:
            y_start, y_end = y[0], y[1]

        for x_change in range(x_start, x_end+1):
            for y_change in range(y_start, y_end+1):
                clay_coords.add((x_change, y_change))
                if ref and ref in buckets:
                    buckets[ref].add((x_change, y_change))
                elif x_start in buckets:
                    buckets[x_start].add((x_change, y_change))
                elif x_end in buckets:
                    buckets[x_end].add((x_change, y_change))
                else:
                    if ref is None:
                        ref = x_start
                    buckets[ref] = {(x_change, y_change)}
                    
        

        x_max = max([x[-1], x_max])
        y_max = max([y[-1], y_max])
        x_min = min([x[0], x_min])

    x_min -= 1
    x_max += 1

    print(buckets)
    input()
               
    print(x_min, x_max, y_min, y_max)
    grid = [[SAND if (i,j) not in clay_coords else CLAY for i in range(x_min, x_max+1)] for j in range(y_min, y_max+1)]

    spring_x = 500 - x_min
    
    grid[0][spring_x] = SPRING

    new_buckets = [set()]
    for b in buckets.values():
        if len(b) == 0:
            continue
        for coord in b:
            new_buckets[-1].add((coord[0]-x_min, coord[1]))
        new_buckets.append(set())

    # check if one bucket is entirely inside another bucket
    new_new_buckets = [set()]
    skip = []
    for b in new_buckets:
        if len(b) == 0 or b in skip: continue
        
        new_new_buckets.append(b)
        for other_b in new_buckets:
            if b == other_b or len(other_b) == 0:    continue

            for coord in other_b:
                
                if coord[0] <= max(b)[0]:
                    if coord[0] >= min(b)[0]:
                        if coord[1] <= max(b, key=lambda y: y[1])[1]:
                            if coord[1] >= min(b, key=lambda y: y[1])[1]:
                                continue
                break
            else:
                #print("merging", new_new_buckets[-1], "with", other_b)
                new_new_buckets[-1] = new_new_buckets[-1].union(other_b)
                
                try:
                    new_new_buckets.remove(other_b)
                    skip.append(other_b)
                except ValueError:
                    pass

    buckets = new_new_buckets
        

    
    return grid, (spring_x, 0)

def write(grid, i ):
    file = open(f"day17vis_frame{i}.txt", "w")
    for y, row in enumerate(grid):
    
        file.write(str(y).zfill(4))
        for x, cell in enumerate(row):           

        
            file.write(cell)

        file.write("\n")
    file.close()
    

def display(grid, start_x=0, start_y=0, stop_y=9999):
    #file = open("day17vis.txt", "w")
    for y, row in enumerate(grid):
        if y < start_y or y > stop_y:
            continue
        print(str(y).zfill(4), end=" ")
        #file.write(str(y).zfill(2))
        for x, cell in enumerate(row):
            if x < start_x:
                continue
            for drop in water:
                if drop == (x, y):
                    cell = "w"

            print(cell, end="")
            #file.write(cell)
        print()
        #file.write("\n")
    #file.close()
    #input("output")

water = set()

counter = 0

class Stream:



    def __init__(self, x, y):
        global counter
        self.x, self.y = x, y
        self.end = False
        self.bucket = None
        
        
        self.id = counter
        counter += 1

    def check(self, grid, ny, nx, item):
        if ny < len(grid) and nx < len(grid[0]):
            return grid[ny][nx] == item
        return False

    def flow(self, grid):
        x, y = self.x, self.y

        new_streams = []

        if not self.end:


            ny = y + 1
            nx = x

            if ny >= len(grid) or nx >= len(grid[0]):
                self.end = True
                print("out of bounds")
                return []

            

            if grid[ny][nx] == SAND:

                grid[ny][nx] = "|"

                self.x, self.y = nx, ny

            elif grid[ny][nx] in (STILL, CLAY):

                clay_y = ny

                while grid[clay_y][nx] != CLAY:
                    clay_y += 1


                for bucket_index, bucket_contents in enumerate(buckets):
                    if (nx, clay_y) in bucket_contents:
                        bucket_id = bucket_index
                        break
                else:
                    print(clay_y, nx, grid[clay_y][nx])
                    raise Exception("Bucket not found..")
                        
                if self.bucket is None:
                    self.bucket = bucket_id
                    print(f"{self.id} reached bucket {bucket_id}")


                bucket_closed = bucket_map.get(bucket_id)
                if bucket_closed == True:
                    print(bucket_map)
                    print(bucket_id, "already springed out")
                    input()
                    self.end = True
                    return []
                
                bucket_map[bucket_id].append(self)

                # fill as far left as possible

                for direction in [-1, +1]:
                    nx = x
                    ny = y
                    while grid[ny][nx] != CLAY:

                        if ny == 179:
                            print(f"{self.id} doing the flood fill why?")
                        grid[ny][nx] = "~"
                        nx += direction
                        if nx == 0 or nx == len(grid[0]):
                            break
                        if self.check(grid, ny+1, nx, FLOW):
                            print("Stream overlap")
                            self.end = True
                            grid[ny][nx] = SAND
                            break
                        elif self.check(grid, ny+1, nx, SAND):
                            self.end = True
                            

                            if type(bucket_map[self.bucket]) == bool:
                                print("Already closed")
                                continue

                            grid[ny][nx] = "|"
                            
                            for feeder in bucket_map[self.bucket]:
                                if not feeder.end:
                                    print("Feeders at this bucket", bucket_map[self.bucket])
                                    print("killed", feeder.id, "because new spring at bucket", self.bucket, "spring y", ny)

                                    feeder.end = True

                            
                            
                            ns = Stream(nx, ny)
                            print("started", ns.id, "at", nx, ny)
                            new_streams.append(ns)
                            break
                        

     

                self.y -= 1

        if len(new_streams) > 0:
            print("Close bucket" , bucket_id)
            bucket_map[self.id] = True

        return new_streams
      


        



        

def final_count(grid):
    print(grid)
    return sum([row.count(STILL) + row.count(FLOW) for row in grid])
        
            
bucket_map = defaultdict(list)

def solve(data):
    count = 0
    global grid

    grid, spring_loc = render(data)


    

    streams = [Stream(*spring_loc)]
    i = 0
    new_streams = []

    print(buckets)
    while True:

        for stream in streams:

            

            for new in stream.flow(grid):
                
                    
                new_streams.append(new)
                #print("New stream")

            
            i += 1
                
            if i > 700 and i < 800 and i % 10 == 0:
                    
                write(grid, i)
                print("write", i)
                

       
       

        streams += new_streams
        
        streams = [s for s in streams if not s.end]

        if len(streams) == 0:
            write(grid, "Final")
            return final_count(grid)

        
        




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

        
    write(grid, "END")
