import re
from itertools import product
from operator import attrgetter, itemgetter
from collections import defaultdict, deque, namedtuple
from heapq import heappush, heappop
import contextlib
from math import ceil

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

State = namedtuple("State", ("pos", "equip"))
Nodes = namedtuple("Nodes", ("time", "state", "previous"))

class Pos:
    __slots__ = ['x', 'y', 'z']
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Pos({self.x}, {self.y}, {self.z})"

    def __eq__(self, o):
        return self.x==o.x and self.y==o.y and self.z==o.z
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, o):
        return Pos(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o):
        return Pos(self.x-o.x, self.y-o.y, self.z-o.z)
    def __floordiv__(self, n):
        return Pos(round(self.x/n), round(self.y/n), round(self.z/n))
    def __mul__(self, n):
        return Pos(self.x*n, self.y*n, self.z*n)
    
    def dist(self, o):
        return sum(abs(d) for d in (self.x-o.x, self.y-o.y, self.z-o.z))

class Bot:
    __slots__ = ['pos', 'range']
    def __init__(self, pos, trange):
        self.pos = pos
        self.range = trange
    
    def __repr__(self):
        return f"Bot({self.pos}, {self.range})"

    def __floordiv__(self, n):
        return Bot(self.pos//n, ceil(self.range/n)+1)

    def in_range(self, o):
        if isinstance(o, Bot):
            o = o.pos
        return self.pos.dist(o) <= self.range

def count_bots_inrange(bots, maxr):
    count = 0
    for bot in bots:
        if maxr.in_range(bot):
            count += 1
    return count

def count_inrange(bots, pos):
    count = 0
    for bot in bots:
        if bot.in_range(pos):
            count += 1
    return count

bots = []
with open("input.txt", "r") as f:
    for line in f:
        x, y, z, r = qp(line)
        bots.append(Bot(Pos(x, y, z), r))
bots.sort(key=attrgetter('range'))
maxr = bots[-1]

print (f"Num in range of {maxr}: {count_bots_inrange(bots, maxr)}")

coords = set([Pos(0, 0, 0)])
for div in range(8, 0, -1):
    ncoords = []
    nbots = [bot//(10**div) for bot in bots]
    for coord in coords:
        for npos in product(range(-10, 11), range(-10, 11), range(-10, 11)):
            npos = coord + Pos(*npos)
            ncoords.append((count_inrange(nbots, npos), npos*10))
    mint = max(ncoords, key=itemgetter(0))
    coords = set(x[1] for x in ncoords if x[0] == mint[0])
    print(div, coords, mint)

ncoords = []
for coord in coords:
    for npos in product(range(-10, 11), range(-10, 11), range(-10, 11)):
        npos = coord + Pos(*npos)
        ncoords.append((count_inrange(bots, npos), npos))
mint = max(ncoords, key=itemgetter(0))
coords = set(x[1] for x in ncoords if x[0] == mint[0])
print(div, coords, mint)

for coord in coords:
    print(coord, coord.x+coord.y+coord.z)