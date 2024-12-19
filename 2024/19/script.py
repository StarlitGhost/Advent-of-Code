from GhostyUtils import aoc
from functools import cache
import re


"""
@cache
def validate(design: str, patterns: frozenset[str]) -> bool:

    if design in patterns:
        if aoc.args.verbose or aoc.args.progress:
            print(f"{design} - found")
        return True
    else:
        # try all splits
        valid = False
        for i in range(1, len(design)-1):
            valid = validate(design[:i], patterns) and validate(design[i:], patterns)
            if valid:
                break
        return valid

    return False
    """


def validate(design: str, patterns: frozenset[str]) -> bool:
    pattern = re.compile(r"^(" + r'|'.join(patterns) + r")+$")
    return re.match(pattern, design)


def main():
    patterns, designs = aoc.read_sections()
    patterns = frozenset(patterns.split(', '))
    designs = designs.splitlines()

    valid = 0
    for design in designs:
        if validate(design, patterns):
            if aoc.args.verbose or aoc.args.progress:
                print(f"1 - {design}")
            valid += 1
        else:
            if aoc.args.verbose or aoc.args.progress:
                print(f"0 - {design}")

    print(f"p1: {valid}")


if __name__ == "__main__":
    main()
