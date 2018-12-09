import re
from collections import defaultdict, Counter
from functools import partial
import numpy as np
import itertools

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

coords = []
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        coords.append(qp(line))

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

grid = np.ndarray(np.max(coords, 0), dtype=np.int32)
for c_coord in itertools.product(*(range(i) for i in grid.shape)):
    s, m, pos = 0, np.inf, 0
    seen = False
    for i, d in enumerate(dist(c_coord, p) for p in coords):
        s += d
        if d < m:
            m = d
            pos = i
            seen = False
        elif d == m:
            seen = True
    if seen:
        grid[c_coord] = -1
    else:
        grid[c_coord] = pos

# Exclude edges
edges = Counter(itertools.chain(grid[0,:], grid[:, 0], grid[-1,:], grid[:,-1]))
edge_nos = set(edges.keys())
print(edge_nos)

counts = Counter(grid.flatten().tolist())
#idx, counts = np.unique(grid, return_counts=True)
m, i = 0, 0
for cidx, count in counts.items():
    if cidx in edge_nos:
        continue
    if count < m:
        continue
    i = cidx
    m = count

print(counts)
print(f"Position was {i} with count {m}")