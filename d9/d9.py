import re
from collections import defaultdict, Counter
from functools import partial
import itertools

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

with open("input.txt", "r") as f:
    num_p, last_m = qp(f.read())
    last_m *= 100

class Node:
    def __init__(self, val):
        self.val = val
        self.prev = self
        self.next = self
class LL:
    def __init__(self):
        self.start = Node(0)
        self.curr = self.start

    def add_after(self, new_node):
        new_node.next = self.curr.next
        new_node.prev = self.curr
        self.curr.next.prev = new_node
        self.curr.next = new_node
        self.curr = new_node
        return self

    def add_before(self, new_node):
        new_node.next = self.curr
        new_node.prev = self.curr.prev
        self.curr.prev.next = new_node
        self.curr.prev = new_node
        self.curr = new_node
        return self

    def remove(self):
        r_node = self.curr
        prev_node = self.curr.prev
        next_node = self.curr.next

        prev_node.next = next_node
        next_node.prev = prev_node

        r_node.prev = r_node
        r_node.next = r_node

        self.curr = next_node
        return r_node

    def go_forward(self, n):
        for _ in range(n):
            self.curr = self.curr.next
        return self

    def go_back(self, n):
        for _ in range(n):
            self.curr = self.curr.prev
        return self

    def print_list(self, player):
        c_marble = self.start
        print(f"[{player}] {c_marble.val}", end=" ")
        c_marble = c_marble.next
        while c_marble != self.start:
            if self.curr == c_marble:
                print(f"({c_marble.val})", end=" ")
            else:
                print(f"{c_marble.val}", end=" ")
            c_marble = c_marble.next
        print("")

players = [0]*num_p
ll = LL()
#ll.print_list("-")
for c_player, n_marble in zip(itertools.cycle(range(num_p)), range(1, last_m+1)):
    if n_marble%23 == 0:
        r_marble = ll.go_back(7).remove()
        players[c_player] += r_marble.val + n_marble
    else:
        ll.go_forward(1).add_after(Node(n_marble))
    #ll.print_list(c_player)
print(f"Winning score: {max(players)}")