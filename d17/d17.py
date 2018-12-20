import re
from itertools import product
from operator import attrgetter
from functools import total_ordering
from collections import defaultdict, deque, namedtuple
import contextlib
import sys, os

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

class Grid:
    def __init__(self):
        self.grid = []
    
    def __repr__(self):
        return f"<Grid({self.xdim}, {self.ydim})>"

    def __getitem__(self, pos):
        return self.grid[pos[1]][pos[0]]
    def __setitem__(self, pos, val):
        if isinstance(pos[0], range) and isinstance(pos[1], range):
            for (x, y) in product(*pos):
                #print(x, y)
                self.grid[y][x] = val
        else:
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

    def print_grid(self, flag=(), psrange=None, perange=None):
        for y, l in enumerate(self.grid):
            if psrange is not None and y < psrange[1]:
                continue
            if perange is not None and y > perange[1]:
                break
            #print(f"{y:3}: ", end="")
            for x, c in enumerate(l):
                if psrange is not None and x < psrange[0]:
                    continue
                if perange is not None and x > perange[0]:
                    break
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
xs = []
ys = []
xrange = [float('inf'), float('-inf')]
yrange = [float('inf'), float('-inf')]
with open("input.txt", "r") as f:
    for y, line in enumerate(f):
        line = line.strip()
        nums = qp(line)
        if line[0] == "x":
            xs.append(range(nums[0], nums[0]+1))
            ys.append(range(nums[1], nums[2]+1))
            if nums[0] < xrange[0]:
                xrange[0] = nums[0]
            if nums[0] > xrange[1]:
                xrange[1] = nums[0]

            if nums[1] < yrange[0]:
                yrange[0] = nums[1]
            if nums[2] > yrange[1]:
                yrange[1] = nums[2]
        else:
            xs.append(range(nums[1], nums[2]+1))
            ys.append(range(nums[0], nums[0]+1))
            if nums[0] < yrange[0]:
                yrange[0] = nums[0]
            if nums[0] > yrange[1]:
                yrange[1] = nums[0]

            if nums[1] < xrange[0]:
                xrange[0] = nums[1]
            if nums[2] > xrange[1]:
                xrange[1] = nums[2]
#print(xs, ys)
print(xrange, yrange)

for y in range(yrange[1]+1):
    grid.append(['.']*(xrange[1]+2))

for pos in zip(xs, ys):
    grid[pos] = '#'

def drop(grid, pos):
    npos = (pos[0], pos[1]+1)
    while npos[1] < grid.ydim and grid[npos] not in ('#', '~'):
        if grid[npos] == "|":
            return "DONE"
        pos = npos
        grid[npos] = '|'
        npos = (npos[0], npos[1]+1)

    lspread = spread(grid, pos, -1)
    rspread = spread(grid, pos, +1)
    while lspread is not None and rspread is not None:
        grid[range(lspread[0], rspread[0]+1), range(pos[1], pos[1]+1)] = "~"
        pos = (pos[0], pos[1]-1)
        lspread = spread(grid, pos, -1)
        rspread = spread(grid, pos, +1)

def spread(grid, pos, sdir):
    lpos = pos
    while grid[lpos] not in ("#", '~'):
        grid[lpos] = '|'
        pos = lpos

        if lpos[1]+1 == grid.ydim:
            return None
        elif grid[lpos[0], lpos[1]+1] == ".":
            drop(grid, lpos)
            return None
        elif grid[lpos[0], lpos[1]+1] == "|":
            return None
        lpos = (lpos[0]+sdir, lpos[1])
    return pos

print(grid.xdim, grid.ydim)
print()
drop(grid, (500, 0))
with open("out.txt", "w") as f:
    with contextlib.redirect_stdout(f):
        grid.print_grid(psrange=(350, 0), flag=((500, 0),))

count = 0
for pos in product(range(grid.xdim), range(yrange[0], yrange[1]+1)):
    if grid[pos] in ('~',):
        count += 1

print(f"Total water: {count}")