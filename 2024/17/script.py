from GhostyUtils import aoc
from dataclasses import dataclass
import operator
from typing import Callable


@dataclass
class Registers:
    A: int
    B: int
    C: int


def combo(operand: int, regs: Registers) -> int:
    match operand:
        case 0: return 0
        case 1: return 1
        case 2: return 2
        case 3: return 3
        case 4: return regs.A
        case 5: return regs.B
        case 6: return regs.C
        case 7: assert False


def process(program: list[int], regs: Registers, output: Callable):
    i_ptr = 0

    while True:
        if i_ptr >= len(program):
            break

        instr = program[i_ptr]
        operand = program[i_ptr+1]

        match instr:
            case 0:  # adv (A division by combo operand, store in A)
                regs.A = regs.A // (2 ** combo(operand, regs))
                i_ptr += 2
            case 1:  # bxl (bitwise xor of B and literal operand, store in B)
                regs.B = operator.xor(regs.B, operand)
                i_ptr += 2
            case 2:  # bst (combo operand modulo 8, store in B)
                regs.B = combo(operand, regs) % 8
                i_ptr += 2
            case 3:  # jnz (jump to literal operand if A non-zero)
                if regs.A == 0:
                    i_ptr += 2
                else:
                    i_ptr = operand
            case 4:  # bxc (bitwise xor of B and C, store in B)
                regs.B = operator.xor(regs.B, regs.C)
                i_ptr += 2
            case 5:  # out (output combo operand modulo 8)
                output(combo(operand, regs) % 8)
                i_ptr += 2
            case 6:  # bdv (A division by combo operand, store in B)
                regs.B = regs.A // (2 ** combo(operand, regs))
                i_ptr += 2
            case 7:  # cdv (A division by combo operand, store in C)
                regs.C = regs.A // (2 ** combo(operand, regs))
                i_ptr += 2


def read_regs(registers: str) -> Registers:
    a, b, c = (r.split(': ') for r in registers.splitlines())
    regs = Registers(int(a[1]), int(b[1]), int(c[1]))
    return regs


def main():
    registers, program = (section.strip() for section in aoc.read_sections())
    regs = read_regs(registers)
    program = list(map(int, program.split(': ')[1].split(',')))

    output = []
    process(program, regs, output=output.append)
    print(f"p1: {','.join(map(str, output))}")


if __name__ == "__main__":
    main()
