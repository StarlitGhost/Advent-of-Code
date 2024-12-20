from GhostyUtils import aoc
import math
from collections import Counter, defaultdict


aoc.argparser.add_argument("-n", "--num_blinks", default=0, type=int,
                           help="number of times to blink")


def num_digits(value: int) -> int:
    return int(math.log10(value)) + 1


def split(value: int) -> tuple[int, int]:
    tens_place = 10 ** (num_digits(value) // 2)
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


def main():
    start_stones = Counter([int(stone) for stone in aoc.read().split()])
    if aoc.args.verbose:
        print(start_stones)

    if aoc.args.num_blinks > 0:
        stones = blink_n_times(start_stones, aoc.args.num_blinks)
        print(f"{aoc.args.num_blinks} blinks: {sum(stones.values())}")

        exit(0)

    stones = blink_n_times(start_stones, 25)
    print(f"p1: {sum(stones.values())}")

    stones = blink_n_times(stones, 50)
    print(f"p2: {sum(stones.values())}")


if __name__ == "__main__":
    main()
