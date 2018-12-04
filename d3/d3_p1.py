import numpy as np
import re

fabric = np.full((1000, 1000), 0, dtype=np.int32)

with open("input.txt", "r") as inp:
    pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    for line in inp:
        if not inp:
            continue
        serial, x, y, w, h = (int(t) for t in pattern.findall(line)[0])
        fabric[x:x+w,y:y+h] += 1

print(f"Overlaps: {np.count_nonzero(fabric >= 2)}")