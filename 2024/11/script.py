from GhostyUtils import aoc
import math
from functools import cache
from collections import Counter, defaultdict


@cache
def num_digits(value: int) -> int:
    return int(math.log10(value)) + 1


@cache
def split(value: int) -> tuple[int, int]:
    digits = num_digits(value)
    tens_place = 10 ** (digits//2)
    l_value = value // tens_place
    r_value = value - (l_value * tens_place)
    return (l_value, r_value)


def blink(stones: dict[int, int]) -> dict[int, int]:
    new_stones = defaultdict(int)
    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count
        elif num_digits(stone) % 2 == 0:
            l_stone, r_stone = split(stone)
            new_stones[l_stone] += count
            new_stones[r_stone] += count
        else:
            new_stones[stone * 2024] += count

    return new_stones


def blink_n_times(stones: dict[int, int], n: int) -> dict[int, int]:
    for _ in range(n):
        stones = blink(stones)

        if aoc.args.verbose:
            print(stones)

    return stones


def num_stones(stones: dict[int, int]) -> int:
    return sum(count for _, count in stones.items())


def main():
    start_stones = Counter([int(stone) for stone in aoc.read().split()])
    if aoc.args.verbose:
        print(start_stones)

    stones = blink_n_times(start_stones, 25)
    print(f"p1: {num_stones(stones)}")

    stones = blink_n_times(start_stones, 75)
    print(f"p2: {num_stones(stones)}")


if __name__ == "__main__":
    main()
