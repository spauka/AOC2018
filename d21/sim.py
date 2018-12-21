# Initial Conditions
v0 = 0
v1 = 0
v5 = 65536
v3 = 5557974

seen = set()
seen_sorted = []

while True:
    v3 = (v5 & 255) + v3
    v3 = v3 & 16777215
    v3 = v3 * 65899
    v3 = v3 & 16777215

    if 256 > v5:
        if v3 in seen:
            print(seen_sorted[-1])
            break
        seen.add(v3)
        seen_sorted.append(v3)

        v5 = v3 | 65536
        v3 = 5557974
        continue
    
    v2 = 0
    v5 //= 256