import re
from collections import defaultdict, Counter, deque
from functools import partial
from itertools import starmap, product

class expanding_list(list):
    def __getitem__(self, i):
        if not isinstance(i, slice):
            return super().__getitem__(i)

        start, stop = i.start, i.stop
        padstart, padstop = 0, 0
        if start < 0:
            padstart = abs(start)
            start = 0
        if stop >= len(self):
            padstop = min(stop - len(self), stop-start)
        ret = [False]*padstart + super().__getitem__(slice(start, stop)) + [False]*padstop
        return ret
    
    def __setitem__(self, i, val):
        if i >= len(self):
            if val:
                while(len(self) < i):
                    self.append(False)
                self.append(val)
            return
        super().__setitem__(i, val)
    
    def copy(self):
        return expanding_list(super().copy())

rules = defaultdict(lambda: False)
initial_state = expanding_list()
padl = 10

initial_state.extend([False]*padl)
with open("input.txt", "r") as f:
    line = f.readline()
    for c in line.strip().split()[-1]:
        initial_state.append(c == "#")

    for line in f:
        if not line.strip():
            continue
        rule, new = re.findall("([.#]*) => ([.#])", line)[0]
        rules[tuple(x=='#' for x in rule)] = new == '#'

def print_state(l, generation):
    print(f"{generation:3}: {''.join('#' if x else '.' for x in l)} ({score(l):6})")
def print_count(n):
    print(f"{'':3}: {' '*(n)}*")
def score(l):
    s = 0
    for i, v in enumerate(l):
        if v:
            s += i-padl
    return s

# Run for 20 generations
print_count(padl)
print_state(initial_state, 0)

p_score = 0
p_diff = 0
diff = -1
stable_iter = 0
while diff != p_diff:
    next_state = initial_state.copy()
    for j in range(-2, len(initial_state)+5):
        #if (j >= 208):
            #print(tuple(initial_state[j-2:j+3]), rules[tuple(initial_state[j-2:j+3])])
        next_state[j] = rules[tuple(initial_state[j-2:j+3])]
    initial_state = next_state.copy()

    n_score = score(initial_state)
    p_diff = diff
    diff = n_score-p_score
    #print(p_score, n_score, n_score-p_score)
    p_score = n_score
    stable_iter += 1
    print_state(initial_state, stable_iter)
    if stable_iter > 200:
        break

f_score = p_score + diff*(50_000_000_000-stable_iter)
print(f"Final score: {f_score}")