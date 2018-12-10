import re
from collections import defaultdict, Counter, deque
from functools import partial
import itertools

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

with open("input.txt", "r") as f:
    num_p, last_m = qp(f.read())
    last_m *= 100

players = [0]*num_p
ll = deque((0,), last_m+1)
for c_player, n_marble in zip(itertools.cycle(range(num_p)), range(1, last_m+1)):
    if n_marble%23 == 0:
        ll.rotate(7)
        players[c_player] += ll.popleft() + n_marble
    else:
        ll.rotate(-2)
        ll.appendleft(n_marble)
print(f"Winning score: {max(players)}")