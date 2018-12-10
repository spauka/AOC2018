import re
from collections import defaultdict, Counter, deque
from functools import partial
from itertools import starmap

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

points, velocities = [], []
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        line = qp(line)
        points.append(line[:2])
        velocities.append(line[-2:])

def print_grid(points):
    offs = tuple(starmap(min, zip(*points)))
    extent = tuple(a-b+1 for a, b in zip(starmap(max, zip(*points)), offs))
    arr = [['.']*extent[1] for _ in range(extent[0])]
    for point in points:
        x, y = tuple(a-b for a, b in zip(point, offs))
        arr[x][y] = "#"
    for line in zip(*arr):
        print("".join(line))

count = 0
cextent = (float("inf"), float("inf"))
nextent = tuple(a-b for a, b in zip(starmap(max, zip(*points)), starmap(min, zip(*points))))

ppoints = points.copy()
while all(a<b for a, b in zip(nextent, cextent)):
    cextent = nextent
    for i, (point, velocity) in enumerate(zip(points, velocities)):
        ppoints[i] = point
        points[i] = tuple(a+b for a, b in zip(point, velocity))
    nextent = tuple(a-b for a, b in zip(starmap(max, zip(*points)), starmap(min, zip(*points))))
    count += 1
print("DONE")

print_grid(ppoints)
print(f"Number of seconds to message: {count-1}")