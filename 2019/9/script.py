from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


def main():
    inputs = [2, 1]
    output = []
    cpu = IntCode(aoc.read(), input=inputs.pop, output=output.append)

    cpu.process()
    print('p1:', output)
    output.clear()

    cpu.reset()
    cpu.process()
    print('p2:', output)


if __name__ == "__main__":
    main()
