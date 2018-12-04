import numpy as np
import re

fabric = np.full((1000, 1000), 0, dtype=np.int32)
claims = {}
good_claims = []

with open("input.txt", "r") as inp:
    pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    for line in inp:
        if not inp:
            continue
        serial, x, y, w, h = (int(t) for t in pattern.findall(line)[0])
        claims[serial] = (x, y, w, h)

        if np.all(fabric[x:x+w,y:y+h] == 0):
            fabric[x:x+w,y:y+h] = serial
            good_claims.append(serial)
        else:
            for s in np.unique(fabric[x:x+w,y:y+h]):
                try:
                    good_claims.remove(s)
                except ValueError:
                    pass
            fabric[x:x+w,y:y+h] = serial

print(f"Good claims: {good_claims}")