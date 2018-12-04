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

m_sleep = []
for i, guard in enumerate(guards):
    mi = np.argmax(guards[guard])
    m_sleep.append((mi, guards[guard][mi], mi*guard))
most_sleeper = max(m_sleep, key=lambda x: x[1])
print(f"Guard {most_sleeper[0]} for {most_sleeper[1]} minutes: {most_sleeper[2]}")