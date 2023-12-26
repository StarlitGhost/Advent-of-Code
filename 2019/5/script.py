from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


if __name__ == "__main__":
    inputs = [5, 1]
    outputs = []
    cpu = IntCode(aoc.read(), input=inputs.pop, output=outputs.append)

    cpu.process()
    print('p1:', outputs[-1])

    cpu.reset()

    cpu.process()
    print('p2:', outputs[-1])
