import re
from collections import defaultdict, Counter
from functools import partial
import numpy as np
import itertools

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

edges = []
vertices = set()
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        edges.append(tuple(re.findall(r" ([A-Z]) ", line)))
        i, o = edges[-1]
        vertices.add(i)
        vertices.add(o)

print(edges, vertices)

def has_in(V, edges):
    for _, o in edges:
        if V == o:
            return True
    return False

def topo_sort(vertices, edges):
    vertices = set(vertices)
    edges = list(edges)

    sort = []
    while vertices:
        c_sort = [V for V in vertices if not has_in(V, edges)]
        c_sort.sort()
        V = c_sort[0]
        
        edges = [edge for edge in edges if edge[0] != V]
        
        vertices.discard(V)
        sort.append(V)
    return sort

print("".join(topo_sort(vertices, edges)))

def free_worker(workers):
    for i, (job,_) in enumerate(workers):
        if job == None:
            return i
    return None

def assemble(vertices, edges, workers=5, static_cost=61):
    vertices = set(vertices)
    edges = list(edges)

    tot_time = 0
    workers = [(None, 0)]*workers

    while True:
        # Figure out the next vertices
        avail = [V for V in vertices if not has_in(V, edges)]
        avail.sort()
        print(f"Jobs available: {avail}")

        # Assign work
        next_worker = free_worker(workers)
        while next_worker is not None and avail:
            work = avail.pop(0)
            vertices.discard(work)
            workers[next_worker] = (work, static_cost+ord(work)-ord('A'))
            next_worker = free_worker(workers)
        print(f"Workers: {workers}")
        
        # Remove shortest remaining job
        work, time = min((worker for worker in workers if worker[0] is not None), key=lambda x: x[1])
        tot_time += time
        for i, (cw, ct) in enumerate(workers):
            if cw is None:
                continue
            if ct-time == 0:
                print(f"Done step {cw}, time is {tot_time}")
                workers[i] = (None, 0)
                edges = [edge for edge in edges if edge[0] != cw]
            else:
                workers[i] = (cw, ct-time)
        
        # If there are no remaining vertices we are done, add the last remaining time!
        if not vertices:
            work, time = max(workers, key=lambda x: x[1])
            tot_time += time
            break
    return tot_time

print(f"Total time: {assemble(vertices, edges)}")