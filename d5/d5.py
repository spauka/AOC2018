import re
from collections import defaultdict
from functools import partial
import numpy as np
import string

with open("input.txt", "r") as inp:
    inp_poly = inp.read().strip()

def react(polymer):
    old_polymer = 0
    while old_polymer != len(polymer):
        i = 1
        old_polymer = len(polymer)
        while i < len(polymer):
            c1 = polymer[i-1]
            c2 = polymer[i]
            c1_case = c1.isupper()
            c2_case = c2.isupper()
            if c1_case != c2_case and c1.lower() == c2.lower():
                polymer = polymer[:i-1] + polymer[i+1:]
            else:
                i += 1
    return len(polymer)

print(f"Size is: {react(inp_poly)}")

repl = np.ndarray(26, dtype=np.int32)
for i, char in enumerate(string.ascii_lowercase):
    new_poly = inp_poly.replace(char, '').replace(char.upper(), '')
    repl[i] = react(new_poly)
    print(f"Char: {char} leads to {repl[i]}")
print(repl)
print(f"remove {string.ascii_lowercase[np.argmin(repl)]} to get length {np.min(repl)}")