from collections import Counter

n_two = 0
n_three = 0
with open("input.txt", "r") as inputFile:
    for line in inputFile:
        if not line:
            continue
        c = Counter(line.strip())
        if 2 in c.values():
            n_two += 1
        if 3 in c.values():
            n_three += 1
print(f"Checksum: {n_two*n_three}")
