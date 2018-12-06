import re
from collections import defaultdict
from functools import partial
import numpy as np
import itertools

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

coords = []
with open("input_jh.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        coords.append(qp(line))
coords = np.array(coords, dtype=np.int32)

def dist(p1, p2):
    return sum(abs(a-b) for a, b in zip(p1, p2))

grid = np.ndarray(np.max(coords, 0), dtype=np.int32)

for c_coord in itertools.product(*(range(i) for i in grid.shape)):
    dists = sum(dist(c_coord, p) for p in coords)
    grid[c_coord] = dists
        
grid[np.where(grid < 10000)] = 1
grid[np.where(grid >= 10000)] = 0

print(grid)
print(np.sum(grid))