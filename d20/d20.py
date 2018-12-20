from collections import deque, namedtuple
import sys

class Node:
    def __init__(self, curr, next):
        self.curr = curr
        self.next = next
    def __repr__(self):
        return f"<Node({self.curr} -> {self.next})>"

def parse(inp, end="$"):
    if not inp:
        return tuple()

    curr = Node("", None)
    options = [curr]
    
    while inp[0] != end:
        c = inp.popleft()
        if c == "(":
            nextnode = parse(inp, ")")
            curr.next = nextnode
            curr = Node("", None)
            nextnode.next = curr
        elif c == "|":
            curr = Node("", None)
            options.append(curr)
        else:
            curr.curr += c
    inp.popleft()

    if len(options) == 1:
        return options[0]
    else:
        return Node(options, None)

def follow_paths(cpos, tree, leafs, seen, path='', dist=0):
    if tree is None:
        #print(dist, path)
        return cpos, dist, path
    #print(f"follow({tree.curr}, {cpos}, {path}, {dist})")
    
    if isinstance(tree.curr, str):
        for c in tree.curr:
            if   c == "E": npos = (cpos[0]+1, cpos[1])
            elif c == "W": npos = (cpos[0]-1, cpos[1])
            elif c == "N": npos = (cpos[0], cpos[1]-1)
            elif c == "S": npos = (cpos[0], cpos[1]+1)
            path += c
            if npos in seen:
                leafs.append((dist, path))
                dist, path = seen[npos]
            else:
                dist += 1
                seen[npos] = (dist, path)
            cpos = npos
        return follow_paths(cpos, tree.next, leafs, seen, path, dist)
    elif isinstance(tree.curr, list):
        if any(i.curr == "" for i in tree.curr):
            for i in tree.curr:
                follow_paths(cpos, i, leafs, seen, path, dist)
            lpaths = [(cpos, dist, path)]
        else:
            lpaths = list(follow_paths(cpos, i, leafs, seen, path, dist) for i in tree.curr)

        paths = []
        for npos, d, npath in lpaths:
            paths.append(follow_paths(npos, tree.next, leafs, seen, npath, d))

        maxdist = -1
        for npos, d, npath in paths:
            if d > maxdist:
                cpos = npos
                maxdist = d
                path = npath
        dist = maxdist
        
        return cpos, dist, path

with open("input.txt", "r") as f:
    inp = deque(f.read().strip())
inp.popleft()
inp = parse(inp)
print()
#print(f"Inp: {inp}")
print()

leafs = []
seen = {(0,0): (0, '')}
print(follow_paths((0, 0), inp, leafs, seen))
print(max(leafs))

count = 0
for pos, (dist, path) in seen.items():
    if dist >= 1000:
        count += 1
print(f"Count: {count}")