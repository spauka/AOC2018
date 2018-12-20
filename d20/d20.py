from collections import deque, namedtuple
from operator import itemgetter

class Node:
    def __init__(self, curr, next):
        self.curr = curr
        self.next = next
        self.loopy = False
    def __repr__(self):
        return f"<Node({self.curr} -> {self.next})>"

def parse(inp, end="$"):
    curr = Node("", None)
    options = [curr]
    
    while inp[0] != end:
        c = inp.popleft()
        if c == "(":
            curr.next = parse(inp, ")")
            curr.next.next = Node("", None)
            curr = curr.next.next
        elif c == "|":
            curr = Node("", None)
            options.append(curr)
        else:
            curr.curr += c
    inp.popleft()

    if len(options) == 1:
        return options[0]
    else:
        newnode = Node(options, None)
        if any(n.curr == "" for n in options):
            newnode.loopy = True
        return newnode

def follow_paths(cpos, tree, seen, path='', dist=0):
    if tree is None:
        return cpos, dist, path
    
    if isinstance(tree.curr, str):
        for c in tree.curr:
            if   c == "E": npos = (cpos[0]+1, cpos[1])
            elif c == "W": npos = (cpos[0]-1, cpos[1])
            elif c == "N": npos = (cpos[0], cpos[1]-1)
            elif c == "S": npos = (cpos[0], cpos[1]+1)
            if npos in seen:
                dist, path = seen[npos]
            else:
                dist += 1
                path += c
                seen[npos] = (dist, path)
            cpos = npos
        return follow_paths(cpos, tree.next, seen, path, dist)
    elif isinstance(tree.curr, list):
        if tree.loopy: # If the options are loopy, let's follow them to find leaf nodes, otherwise skip this node
            for i in tree.curr:
                follow_paths(cpos, i, seen, path, dist)
            return follow_paths(cpos, tree.next, seen, path, dist)

        # Alternatively we have to follow all alternative paths
        lpaths = list(follow_paths(cpos, i, seen, path, dist) for i in tree.curr)
        paths = []
        for npos, d, npath in lpaths:
            paths.append(follow_paths(npos, tree.next, seen, npath, d))

        return max(paths, key=itemgetter(1))

with open("input.txt", "r") as f:
    inp = deque(f.read().strip())
inp.popleft()
inp = parse(inp)

seen = {(0,0): (0, '')}
follow_paths((0, 0), inp, seen)
print(max(seen.values()))

print(f"Count: {sum(dist >= 1000 for dist, _ in seen.values())}")