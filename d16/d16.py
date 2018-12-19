import re
from enum import Enum, auto
from operator import add, mul, and_, or_, gt, eq

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

def noop(val):
    return val

class ArgType(Enum):
    IMM = auto()
    REG = auto()

class Operation:
    OPERATIONS = []

    def __init__(self, name, opcode, arg_type, action):
        self.name = name
        self.opcode = opcode
        self.arg_type = arg_type
        self.action = action
        Operation.OPERATIONS.append(self)
    
    def __repr__(self):
        return f"Operation({self.name})"

    def get_arg(self, arg_num, state, args):
        if self.arg_type[arg_num] == ArgType.REG:
            return state[args[arg_num+1]]
        elif self.arg_type[arg_num] == ArgType.IMM:
            return args[arg_num+1]
        else:
            raise ValueError("Unknown argument type")

    def apply(self, state, args):
        par_vals = []
        for i, _ in enumerate(self.arg_type):
            par_vals.append(self.get_arg(i, state, args))
        val = int(self.action(*par_vals))
        return state[:args[3]] + (val,) + state[args[3]+1:]

Operation("addr", 0, (ArgType.REG, ArgType.REG), add)
Operation("addi", 0, (ArgType.REG, ArgType.IMM), add)
Operation("mulr", 0, (ArgType.REG, ArgType.REG), mul)
Operation("muli", 0, (ArgType.REG, ArgType.IMM), mul)
Operation("banr", 0, (ArgType.REG, ArgType.REG), and_)
Operation("bani", 0, (ArgType.REG, ArgType.IMM), and_)
Operation("borr", 0, (ArgType.REG, ArgType.REG), or_)
Operation("bori", 0, (ArgType.REG, ArgType.IMM), or_)
Operation("setr", 0, (ArgType.REG,), noop)
Operation("seti", 0, (ArgType.IMM,), noop)
Operation("gtir", 0, (ArgType.IMM, ArgType.REG), gt)
Operation("gtri", 0, (ArgType.REG, ArgType.IMM), gt)
Operation("gtrr", 0, (ArgType.REG, ArgType.REG), gt)
Operation("eqir", 0, (ArgType.IMM, ArgType.REG), eq)
Operation("eqri", 0, (ArgType.REG, ArgType.IMM), eq)
Operation("eqrr", 0, (ArgType.REG, ArgType.REG), eq)

with open("input.txt", "r") as f:
    lines = f.readlines()

# Read lines in fours
print(len(lines), (len(lines)+1)//4)
ops = [tuple(lines[i*4:(i+1)*4-1]) for i in range((len(lines)+1)//4)]

count = 0
mapping = {}

for op in ops:
    before = qp(op[0])
    args = qp(op[1])
    after = qp(op[2])

    valid_states = set()
    for opa in Operation.OPERATIONS:
        new_state = opa.apply(before, args)
        if new_state == after:
            valid_states.add(opa)
    if len(valid_states) >= 3:
        count += 1
    if args[0] in mapping:
        mapping[args[0]].intersection_update(valid_states)
    else:
        mapping[args[0]] = valid_states

cleared = set()
while not all(len(s) == 1 for s in mapping.values()):
    for val, s in mapping.items():
        if len(s) == 1 and val not in cleared:
            cleared.add(val)
            break
    else:
        print("Couldn't disambiguate!")
        exit(0)
    
    for o in mapping:
        if o == val:
            continue
        mapping[o].difference_update(s)

print(f"{count} inputs are valid for more than 3 operators")

for val in mapping:
    mapping[val] = mapping[val].pop()
print(mapping)

with open("input_p.txt", "r") as f:
    state = (0,0,0,0)
    for line in f:
        if not line.strip():
            continue
        p = qp(line)
        state = mapping[p[0]].apply(state, p)
print(state)