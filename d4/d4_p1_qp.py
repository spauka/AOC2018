import re
from collections import defaultdict
from functools import partial
import numpy as np

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

guards = defaultdict(partial(np.zeros, 59))
lines = []
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        m, d, ho, mi = qp(line)[1:5]
        lines.append((m, d, ho, mi, line))
lines.sort()

for m, d, ho, mi, line in lines:
    if "begins shift" in line:
        cguard = qp(line)[-1]
        continue
    
    if "falls asleep" in line:
        asleep = mi
        continue
    
    if "wakes up" in line:
        guards[cguard][asleep:mi] += 1
        continue
    
    print(f"{line} didnt match")

m_sleep = np.ndarray(len(guards))
for i, guard in enumerate(guards):
    m_sleep[i] = np.sum(guards[guard])

most = tuple(guards.keys())[np.argmax(m_sleep)]
most_min = np.argmax(guards[most])

print(f"Guard {most} for {most_min} minutes: {most_min*most}")