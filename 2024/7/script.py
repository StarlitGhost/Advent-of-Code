from GhostyUtils import aoc
import operator
import itertools
from typing import Callable


def calibrate(target: int, operands: list[int], operators: list[Callable]) -> int:
    # try all operators in all positions between operands
    for ops in itertools.product(operators, repeat=len(operands)-1):
        # calculate left-to-right
        result = operands[0]
        for i, op in enumerate(ops):
            result = op(result, operands[i+1])

            # ops only make the result larger,
            # so abort if result is already larger than target
            if result > target:
                break

        if aoc.args().verbose:
            print(f"{target}: {operands} | {ops} -> {result}")

        # return early if we find a calculation that works
        if result == target:
            return target

    # no valid calculation found
    return 0


# concatenate two ints as if they were strings
def concat(l: int, r: int) -> int:
    return int(f"{l}{r}")


def main():
    inputs = aoc.read_lines()

    total = 0
    p2total = 0

    for line in inputs:
        target, operands = line.split(': ')
        target = int(target)
        operands = list(map(int, operands.split(' ')))

        result = calibrate(target, operands, [operator.add, operator.mul])
        total += result

        if result == 0:
            p2total += calibrate(target, operands, [operator.add, operator.mul, concat])

    print(f"p1: {total}")
    print(f"p2: {total + p2total}")


if __name__ == "__main__":
    main()
