from GhostyUtils import aoc
import re


def main():
    instrs = aoc.read()
    muls = re.findall(r"mul\((\d+),(\d+)\)", instrs)
    print("p1:", sum(int(m1) * int(m2) for m1, m2 in muls))


if __name__ == "__main__":
    main()
