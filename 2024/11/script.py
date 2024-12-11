from GhostyUtils import aoc
import math


def num_digits(value: int) -> int:
    return int(math.log10(value)) + 1


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for i, stone in enumerate(stones):
        if stone == 0:
            new_stones.append(1)
        elif num_digits(stone) % 2 == 0:
            digits = num_digits(stone)
            um = 10 ** (digits//2)
            l_stone = stone // um
            r_stone = stone - (l_stone * um)
            new_stones += [l_stone, r_stone]
        else:
            new_stones.append(stone * 2024)

    return new_stones


def main():
    stones = [int(stone) for stone in aoc.read().split()]
    if aoc.args.verbose:
        print(stones)

    for _ in range(25):
        stones = blink(stones)
        if aoc.args.verbose:
            print(stones)
    print(f"p1: {len(stones)}")


if __name__ == "__main__":
    main()
