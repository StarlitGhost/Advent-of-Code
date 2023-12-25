from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


if __name__ == "__main__":
    outputs = []
    cpu = IntCode(aoc.read(), input_gen=(n for n in [1]), output=outputs.append)
    cpu.process()
    print('p1:', outputs[-1])

    outputs = []
    cpu = IntCode(aoc.read(), input_gen=(n for n in [5]), output=outputs.append)
    cpu.process()
    print('p2:', outputs[-1])
