import re
from collections import defaultdict, Counter, deque
from functools import partial
from itertools import starmap, product
import numpy as np

def calc_fuel(x, y, serial=3031):
    rack_id = x + 10
    power = (rack_id*y + serial)*rack_id
    power = int(f"{power:05d}"[-3]) - 5
    return power

grid = []
for Y in range(1, 301):
    line = []
    for X in range(1, 301):
        s = calc_fuel(X, Y, 3031)
        if X > 1:
            s += line[-1]
        line.append(s)
        
    if Y > 1:
        for X in range(1, 301):
            line[X-1] += grid[-1][X-1]
    grid.append(line)

mval = 0
mind = (-1, -1, -1)
for size in range(1, 301):
    for X, Y in product(range(size, 301), range(size, 301)):
        s = grid[Y-1][X-1]
        if Y-size > 0:
            s -= grid[Y-size-1][X-1]
        if X-size > 0:
            s -= grid[Y-1][X-size-1]
        if X-size > 0 and Y-size > 0:
            s += grid[Y-size-1][X-size-1]
        
        if s > mval:
            mval = s
            mind = (X-size+1, Y-size+1, size)
    print(f"Size: {size}, mind: {mind}, mval: {mval}")
            
print(mval, mind)