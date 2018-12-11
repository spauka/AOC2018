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
        line.append(calc_fuel(X, Y, 3031))
    grid.append(line)

for Y in range(0, 3):
    for X in range(0, 3):
        print(grid[Y][X], end=" ")
    print()
exit()

mval = 0
mind = (-1, -1, -1)
for size in range(1,301):
    print(f"Size: {size}, mind: {mind}, mval: {mval}")

    rgrid = []
    for Y in range(1, 301):
        rline = []
        for X in range(1, 301-size-1):
            s = 0
            for XO in range(-1, -1+size+1):
                s += grid[Y-1][XO+X]
            rline.append(s)
        rgrid.append(rline)
    
    for X, Y in product(range(1, 301-size-1), range(1, 301-size-1)):
        s = 0                
        for YO in range(-1, -1+size+1):
            s += rgrid[YO+Y][X-1]
        if s > mval:
            mval = s
            mind = (X, Y, size+1)
            
print(mval, mind)