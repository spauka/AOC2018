import re
from collections import defaultdict, Counter, deque
from functools import partial
from itertools import starmap, product
import numpy as np

def calc_fuel(x, y, serial=3031):
    rack_id = x + 10
    power = (rack_id*y + serial)*rack_id
    power = (int(power/100)%10) - 5
    return power

grid = [[0]*301]
for Y in range(1, 301):
    line = [0]
    for X in range(1, 301):
        s = calc_fuel(X, Y, 3031) + line[-1]
        line.append(s)
        
    for X in range(1, 301):
        line[X] += grid[-1][X]
    grid.append(line)

mval = 0
mind = (-1, -1, -1)
for size in range(1, 301):
    for X, Y in product(range(size, 301), range(size, 301)):
        s = grid[Y][X]
        s -= grid[Y-size][X]
        s -= grid[Y][X-size]
        s += grid[Y-size][X-size]
        
        if s > mval:
            mval = s
            mind = (X-size+1, Y-size+1, size)
    print(f"Size: {size}, mind: {mind}, mval: {mval}")
            
print(mval, mind)