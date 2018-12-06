import re
from collections import defaultdict
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
coords = np.array(coords)

def dist(p1, p2):
    return sum(abs(a-b) for a, b in zip(p1, p2))

grid = np.ndarray(np.max(coords, 0))

for c_coord in itertools.product(*(range(i) for i in grid.shape)):
    dists = np.array(tuple(dist(c_coord, p) for p in coords))
    grid[c_coord] = np.argmin(dists)
    if np.count_nonzero(dists == np.min(dists)) > 1:
        grid[c_coord] = np.nan

# Exclude edges
edges = np.concatenate((grid[0,:], grid[:, 0], grid[-1,:], grid[:,-1]))
edge_nos = np.unique(edges)
print(edge_nos)

for n in edge_nos:
    if np.isnan(n):
        continue
    grid[np.where(grid == n)] = np.nan

idx, counts = np.unique(grid, return_counts=True)
counts = counts[np.where(np.logical_not(np.isnan(idx)))]
idx = idx[np.where(np.logical_not(np.isnan(idx)))]

print(idx, counts)
print(np.max(counts))