from GhostyUtils import aoc


def process(program, regs):
    instr_ptr = 0
    while 0 <= instr_ptr < len(program):
        instr = program[instr_ptr]
        op, arg = instr.split(maxsplit=1)

        reg = None
        offset = None

        if op in ['hlf', 'tpl', 'inc']:
            reg = arg
        elif op in ['jie', 'jio']:
            reg, offset = arg.split(', ')
            offset = int(offset)
        elif op in ['jmp']:
            offset = int(arg)

        match op:
            case 'hlf':
                regs[reg] //= 2
                instr_ptr += 1
            case 'tpl':
                regs[reg] *= 3
                instr_ptr += 1
            case 'inc':
                regs[reg] += 1
                instr_ptr += 1
            case 'jmp':
                instr_ptr += offset
            case 'jie':
                instr_ptr += offset if regs[reg] % 2 == 0 else 1
            case 'jio':
                instr_ptr += offset if regs[reg] == 1 else 1


if __name__ == "__main__":
    program = aoc.read_lines()

    regs = {'a': 0, 'b': 0}
    process(program, regs)
    print(regs['b'])

    regs = {'a': 1, 'b': 0}
    process(program, regs)
    print(regs['b'])
