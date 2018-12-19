from itertools import product
from operator import attrgetter
from functools import total_ordering
from collections import defaultdict, deque, namedtuple

Nodes = namedtuple("Nodes", ("dist", "pos", "previous"))
Action = namedtuple("Action", ("action", "creature", "pos"))

class Grid:
    def __init__(self):
        self.grid = []
        self.creatures = []
    
    def __repr__(self):
        return f"<Grid({self.xdim}, {self.ydim})>"

    def __getitem__(self, pos):
        return self.grid[pos[1]][pos[0]]
    def __setitem__(self, pos, val):
        self.grid[pos[1]][pos[0]] = val

    def append(self, line):
        line = list(line)
        if self.grid:
            if len(line) != self.xdim:
                raise ValueError("Line must be the same length as other lines")
        self.grid.append(line)
    def copy(self):
        new_grid = self.__class__()
        for row in self.grid:
            new_grid.append(row.copy())
        return new_grid

    def neighbours(self, pos):
        possibilities = ((pos[0]-1, pos[1]-1),
                         (pos[0],   pos[1]-1),
                         (pos[0]+1, pos[1]-1),
                         (pos[0]-1, pos[1]),
                         (pos[0]+1, pos[1]),
                         (pos[0]-1, pos[1]+1),
                         (pos[0],   pos[1]+1),
                         (pos[0]+1, pos[1]+1))
        return possibilities
    def neighbours_valid(self, pos):
        return tuple(p for p in self.neighbours(pos) if self.validate_pos(p))
    def validate_pos(self, pos):
        if pos[0] < 0 or pos[0] >= self.xdim:
            return False
        if pos[1] < 0 or pos[1] >= self.ydim:
            return False
        return True

    def count_adjacent(self, pos, find):
        count = 0
        for neighbour in self.neighbours_valid(pos):
            if self[neighbour] == find:
                count += 1
        return count

    def print_grid(self, flag=()):
        for y, l in enumerate(self.grid):
            print(f"{y:3}: ", end="")
            for x, c in enumerate(l):
                if (x, y) in flag:
                    print('!', end="")
                else:
                    print(c, end="")
            print()

    @property
    def xdim(self):
        return len(self.grid[0])
    @property
    def ydim(self):
        return len(self.grid)

grid = Grid()
with open("input.txt", "r") as f:
    for y, line in enumerate(f):
        line = line.strip()
        cline = []
        for x, c in enumerate(line):
            cline.append(c)
        grid.append(cline)
grid.print_grid()

for i in range(1000000000):
    new_grid = grid.copy()
    for pos in product(range(grid.xdim), range(grid.ydim)):
        if grid[pos] == "." and grid.count_adjacent(pos, "|") >= 3:
            new_grid[pos] = "|"
        elif grid[pos] == "|" and grid.count_adjacent(pos, "#") >= 3:
            new_grid[pos] = "#"
        elif grid[pos] == "#" and (grid.count_adjacent(pos, "#") < 1 or grid.count_adjacent(pos, "|") < 1):
            new_grid[pos] = "."
    grid = new_grid

    n_wood, n_lumber = 0, 0
    for pos in product(range(grid.xdim), range(grid.ydim)):
        if grid[pos] == "|":
            n_wood += 1
        elif grid[pos] == "#":
            n_lumber += 1
    print(i+1, n_wood, n_lumber, n_wood*n_lumber)

