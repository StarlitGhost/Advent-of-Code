from GhostyUtils import aoc
import re
import math


def find_muls(stream):
    muls = [tuple(map(int, m[1].split(","))) for m in re.finditer(r"mul\((\d+,\d+)\)", stream)]
    return muls


def find_instrs(stream):
    instrs = [m for m in re.finditer(r"mul\((\d+,\d+)\)|do\(\)|don't\(\)", stream)]
    return instrs


def main():
    stream = aoc.read()

    muls = find_muls(stream)
    print("p1:", sum(l * r for l, r in muls))

    enabled = True
    total = 0
    instrs = find_instrs(stream)
    for instr in instrs:
        if instr[0] == "don't()":
            enabled = False
        elif instr[0] == "do()":
            enabled = True
        elif enabled:
            total += math.prod(map(int, instr[1].split(',')))

    print("p2:", total)


if __name__ == "__main__":
    main()
