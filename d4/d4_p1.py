import re
from collections import defaultdict
from functools import partial
import numpy as np

guards = defaultdict(partial(np.zeros, 59))

lines = []
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        m = re.match(r"\[1518-(\d+)-(\d+) (\d+):(\d+)\]", line)
        m, d, ho, mi = [int(x) for x in m.groups()]
        lines.append((m, d, ho, mi, line))
lines.sort()

for m, d, ho, mi, line in lines:
    match = re.match(r".*Guard #(\d+) begins shift", line)
    if match:
        g = int(match.groups()[0])
        cguard = g
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