import sys
import operator
import itertools


def print_line(line):
    l, op, r, output
    match op:
        case 'AND' | 'OR' | 'LSHIFT' | 'RSHIFT':
            print(f'{l} {op} {r} -> {output}')
        case 'NOT':
            print(f'{op} {r} -> {output}')
        case _:
            print(f'{l} -> {output}')

def not_16b(val):
    return ~val & 0xffff

ops = {'AND': operator.and_,
        'OR': operator.or_,
        'LSHIFT': operator.lshift,
        'RSHIFT': operator.rshift,
        'NOT': not_16b}

def wire_value(wv):
    if wv is None:
        return None
    elif wv in wires:
        return wires[wv]
    elif wv.isnumeric():
        return int(wv)

def process(line):
    l, op, r, output = line
    l = wire_value(l)
    r = wire_value(r)

    match op:
        case 'AND' | 'OR' | 'LSHIFT' | 'RSHIFT':
            if l is not None and r is not None:
                wires[output] = ops[op](l, r)
                return True
        case 'NOT':
            if r is not None:
                wires[output] = ops[op](r)
                return True
        case _:
            if l is not None:
                wires[output] = l
                return True
    return False

def simulate(circuit, wires):
    while True:
        wires_done = len(wires)
        for index, line in enumerate(circuit):
            if line[3] not in wires:
                process(line)
        if len(wires) == wires_done:
            break

    return wires

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    circuit = []

    for line in inputs:
        instr, output = line.split(' -> ')
        
        instr = instr.split(' ')

        l, op, r = None, None, None

        try:
            if len(instr) == 1:
                l = instr[0]
            elif len(instr) == 2:
                op, r = instr
            elif len(instr) == 3:
                l, op, r = instr
        except ValueError as e:
            print(line)
            print(e)

        circuit.append((l, op, r, output))

    wires = {}
    wires = simulate(circuit, wires)

    #for k, v in sorted(wires.items()):
    #    print(f'{k}: {v}')

    print(f"a: {wires['a']}")

    a = wires['a']
    wires = {}
    wires['b'] = a

    wires = simulate(circuit, wires)
    print(f"a: {wires['a']}")
