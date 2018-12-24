import re
from itertools import product
from operator import attrgetter, itemgetter
from collections import defaultdict, deque, namedtuple
from heapq import heappush, heappop
import contextlib

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

State = namedtuple("State", ("pos", "equip"))
Nodes = namedtuple("Nodes", ("time", "state", "previous"))
cmap = ['.', '=', '|']
vequip = [set(("gear", "torch")), set(("none", "gear")), set(("none", "torch"))]

class Grid:
    @classmethod
    def make_grid(cls, xdim, ydim, fill=0):
        grid = cls()
        for _ in range(ydim):
            grid.append([fill]*xdim)
        return grid

    def __init__(self, offs=(0, 0)):
        self.grid = []
        self.offs = (0, 0)
    
    def __repr__(self):
        return f"<Grid({self.xdim}, {self.ydim})>"

    def __getitem__(self, pos):
        return self.grid[pos[1] - self.offs[1]][pos[0] - self.offs[0]]
    def __setitem__(self, pos, val):
        if isinstance(pos[0], slice) and isinstance(pos[1], slice):
            xs, ys = pos
            for (x, y) in product(range(xs.start, xs.stop, xs.step), range(ys.start, ys.stop, ys.step)):
                self.grid[y - self.offs[1]][x - self.offs[0]] = val
        else:
            self.grid[pos[1] - self.offs[1]][pos[0] - self.offs[0]] = val

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
        possibilities = ((pos[0],   pos[1]-1),
                         (pos[0]-1, pos[1]  ),
                         (pos[0]+1, pos[1]  ),
                         (pos[0],   pos[1]+1))
        return possibilities
    def neighbours_valid(self, pos):
        return tuple(p for p in self.neighbours(pos) if self.validate_pos(p))
    def validate_pos(self, pos):
        if pos[0] < 0 or pos[0] >= self.xdim:
            return False
        if pos[1] < 0 or pos[1] >= self.ydim:
            return False
        return True
    def validate_equip(self, equip, pos):
        return equip in vequip[self[pos]%3]

    def count_adjacent(self, pos, find):
        count = 0
        for neighbour in self.neighbours_valid(pos):
            if self[neighbour] == find:
                count += 1
        return count
    
    def calc_d(self, start, target=None):
        visited = {}
        nextnode = [Nodes(0, start, None)]

        while nextnode:
            visiting = heappop(nextnode)
            state = visiting.state
            if state in visited:
                continue
            visited[state] = visiting

            if state == target:
                return visited
            
            # Try changing equipment
            new_equip = vequip[self[state.pos]%3].difference(set((state.equip,))).pop()
            new_state = State(visiting.state.pos, new_equip)

            if new_state not in visited:
                new_node = Nodes(visiting.time+7, new_state, visiting)
                heappush(nextnode, new_node)

            # And visit all neighbours
            for neighbour in self.neighbours_valid(state.pos):
                # Check if we have the correct equipment
                if not self.validate_equip(state.equip, neighbour):
                    continue
                else: # We can move simply
                    new_state = State(neighbour, state.equip)

                    if new_state not in visited:
                        new_node = Nodes(visiting.time+1, new_state, visiting)
                        heappush(nextnode, new_node)

        return visited
    def backtrack(self, end):
        path = deque()
        while end:
            path.appendleft(end.state)
            end = end.previous
        return tuple(path)

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
                    print(cmap[c%3], end="")
            print()

    @property
    def xdim(self):
        return len(self.grid[0])
    @property
    def ydim(self):
        return len(self.grid)

with open("input.txt", "r") as f:
    depth = qp(f.readline())[0]
    tpos = qp(f.readline())

pad = (50, 10)
#pad = (20, 20)
grid = Grid.make_grid(tpos[0]+pad[0]+1, tpos[1]+pad[1]+1, 0)

risk = 0
for pos in product(range(grid.xdim), range(grid.ydim)):
    if pos == (0, 0) or pos == tpos:
        grid[pos] = (0 + depth) % 20183
    elif pos[0] == 0:
        grid[pos] = (pos[1]*48271 + depth) % 20183
    elif pos[1] == 0:
        grid[pos] = (pos[0]*16807 + depth) % 20183
    else:
        grid[pos] = ((grid[pos[0]-1, pos[1]]*grid[pos[0],pos[1]-1]) + depth) % 20183
    
    if pos[0] <= tpos[0] and pos[1] <= tpos[1]:
        risk += grid[pos]%3

#grid.print_grid(flag=(tpos,))
start = State((0, 0), 'torch')
target = State(tpos, 'torch')
visited = grid.calc_d(start, target=target)
print(f"Visited nodes: {len(visited)}")

print(f"Risk: {risk}")
print(f"Quickest Path: {visited[target].time}")
path = grid.backtrack(visited[State(tpos, 'torch')])
#print(f"Path: {path}")
poss = [x.pos for x in path]
f = open("output.txt", "w")
with contextlib.redirect_stdout(f):
    grid.print_grid(tuple(x.pos for x in path))