from GhostyUtils import aoc
from functools import cache


@cache
def validate(design: str, patterns: frozenset[str]) -> bool:
    if design in patterns:
        return True
    else:
        # try all splits
        valid = False
        for i in range(1, len(design)):
            if aoc.args.verbose:
                print(f" trying {design[:i]}-{design[i:]}")
            valid = validate(design[:i], patterns) and validate(design[i:], patterns)
            if valid:
                return True

    return False


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

    if aoc.args.progress:
        print(f"cache: {validate.cache_info().hits} hits, {validate.cache_info().misses} misses")

    print(f"p1: {valid}")


if __name__ == "__main__":
    main()
