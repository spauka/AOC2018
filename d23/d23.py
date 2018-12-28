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

class Pos:
    __slots__ = ['x', 'y', 'z']
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Pos({self.x}, {self.y}, {self.z})"

    def __add__(self, o):
        return Pos(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o):
        return Pos(self.x-o.x, self.y-o.y, self.z-o.z)
    
    def dist(self, o):
        return sum(abs(d) for d in (self.x-o.x, self.y-o.y, self.z-o.z))

class Bot:
    __slots__ = ['pos', 'range']
    def __init__(self, pos, trange):
        self.pos = pos
        self.range = trange
    
    def __repr__(self):
        return f"Bot({self.pos}, {self.range})"

    def in_range(self, o):
        return self.pos.dist(o.pos) <= self.range
    def intersects(self, o):
        return self.pos.dist(o.pos) <= self.range + o.range

bots = []
with open("input.txt", "r") as f:
    for line in f:
        x, y, z, r = qp(line)
        bots.append(Bot(Pos(x, y, z), r))
bots.sort(key=attrgetter('range'))
maxr = bots[-1]
count = 0
for bot in bots:
    if maxr.intersects(bot):
        count += 1
print (f"Num in range of {maxr}: {count}")

def count_intersections(botmax, bots):
    count = 0
    for bot in bots:
        if botmax.intersects(bot):
            count += 1
    return count

botmax = Bot(Pos(0,0,0), 2**64)
while botmax.range > 1:
    print(botmax, count_intersections(botmax, bots))
    offs = botmax.range//2
    poss = [Pos( offs//2, 0, 0),
            Pos(-offs//2, 0, 0),
            Pos(0,  offs//2, 0),
            Pos(0, -offs//2, 0),
            Pos(0, 0,  offs//2),
            Pos(0, 0, -offs//2)]
    botmaxes = [Bot(botmax.pos+pos, offs) for pos in poss]
    botmax = max(botmaxes, key=lambda x: count_intersections(x, bots))
print(botmax, count_intersections(botmax, bots))
print (f"Num in range of {botmax}: {count_intersections(botmax, bots)}")

