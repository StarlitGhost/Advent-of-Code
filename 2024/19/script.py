from GhostyUtils import aoc
from functools import cache


@cache
def validate(design: str, patterns: frozenset[str]) -> int:
    # if there's nothing left of the design after recursively slicing patterns from it,
    # we found a valid arrangement. return 1 to count it in our sum of all arrangements
    if not design:
        return 1

    # try removing all patterns from the start of the design,
    # then recursively do that for each remaining segment of the design
    return sum(validate(design[len(pattern):], patterns)
               for pattern in patterns if design[:len(pattern)] == pattern)


def main():
    patterns, designs = aoc.read_sections()
    patterns = frozenset(patterns.split(', '))
    designs = designs.splitlines()

    valid = 0
    total_arrangements = 0
    for design in designs:
        arrangements = validate(design, patterns)
        if arrangements:
            if aoc.args.verbose or aoc.args.progress:
                print(f"1 - {design} - {arrangements}")
            valid += 1
            total_arrangements += arrangements
        else:
            if aoc.args.verbose or aoc.args.progress:
                print(f"0 - {design}")

    if aoc.args.verbose or aoc.args.progress:
        print(f"validate() {validate.cache_info()}")

    print(f"p1: {valid}")
    print(f"p2: {total_arrangements}")


if __name__ == "__main__":
    main()
