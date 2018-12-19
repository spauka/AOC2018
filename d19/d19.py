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
    INSTR_MAP = {}

    def __init__(self, name, arg_type, action):
        self.name = name
        self.arg_type = arg_type
        self.action = action
        Operation.OPERATIONS.append(self)
        Operation.INSTR_MAP[name] = self
    
    def __repr__(self):
        return f"Operation({self.name})"

    def get_arg(self, arg_num, state, args):
        if self.arg_type[arg_num] == ArgType.REG:
            return state[args[arg_num]]
        elif self.arg_type[arg_num] == ArgType.IMM:
            return args[arg_num]
        else:
            raise ValueError("Unknown argument type")

    def apply(self, state, args):
        par_vals = []
        for i, _ in enumerate(self.arg_type):
            par_vals.append(self.get_arg(i, state, args))
        val = int(self.action(*par_vals))
        state[args[2]] = val
        return state

class Processor:
    def __init__(self, program, instrs=Operation.INSTR_MAP):
        self.ip = 0
        self.ip_map = None
        self.regs = [0]*6
        self.instrs = instrs
        self.program = program

    def run_program(self):
        i = 0
        while self.ip < len(self.program):
            self.exec_instr()
            i += 1
            if i%100000 == 0:
                print(f"Instr: {i:10}")
    
    def exec_instr(self):
        # Update IP register
        if self.ip_map is not None:
            self.regs[self.ip_map] = self.ip
        
        # Execute instruction at IP
        instr, args = self.program[self.ip]
        #print(f"ip={self.ip} {self.state} {instr} {args}", end=" ")
        self.instrs[instr].apply(self.state, args)
        #print(f"{self.state}")

        # Set the IP register back
        if self.ip_map is not None:
            self.ip = self.regs[self.ip_map]
        
        # Increment ip
        self.ip += 1

    @property
    def state(self):
        return self.regs
    @state.setter
    def state(self, val):
        self.regs = val

Operation("addr", (ArgType.REG, ArgType.REG), add)
Operation("addi", (ArgType.REG, ArgType.IMM), add)
Operation("mulr", (ArgType.REG, ArgType.REG), mul)
Operation("muli", (ArgType.REG, ArgType.IMM), mul)
Operation("banr", (ArgType.REG, ArgType.REG), and_)
Operation("bani", (ArgType.REG, ArgType.IMM), and_)
Operation("borr", (ArgType.REG, ArgType.REG), or_)
Operation("bori", (ArgType.REG, ArgType.IMM), or_)
Operation("setr", (ArgType.REG,), noop)
Operation("seti", (ArgType.IMM,), noop)
Operation("gtir", (ArgType.IMM, ArgType.REG), gt)
Operation("gtri", (ArgType.REG, ArgType.IMM), gt)
Operation("gtrr", (ArgType.REG, ArgType.REG), gt)
Operation("eqir", (ArgType.IMM, ArgType.REG), eq)
Operation("eqri", (ArgType.REG, ArgType.IMM), eq)
Operation("eqrr", (ArgType.REG, ArgType.REG), eq)

lines = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line.strip():
            continue
        line = line.split()

        instr, *args = line
        args = tuple(int(x) for x in args)
        lines.append((instr, args))

ip_set = lines.pop(0)
p = Processor(lines)
p.ip_map = ip_set[1][0]
p.state = [1, 0, 0, 0, 0, 0]
p.run_program()
print(f"Final state: {p.state}")