from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


def main():
    output = []
    cpu = IntCode(aoc.read(), input=[1].pop, output=output.append)
    cpu.process()
    print(output)


if __name__ == "__main__":
    main()
