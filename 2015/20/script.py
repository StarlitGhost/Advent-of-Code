import sys
import itertools
import math
from math import log


def robins_inequality(n):
    if 3 <= n <= 5040:
        return math.e * n * log(log(n)) + (0.6483 * n) / log(log(n))
    else:
        return math.e * n * log(log(n))


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))
    min_presents = int(next(inputs))

    houses = [0]*10000000
    min_house = min_presents // 10
    for elf in itertools.count(start=1):
        if elf >= min_house:
            break
        for house_num in range(elf, min_house, elf):
            houses[house_num] += 10*elf
            if houses[house_num] >= min_presents:
                if house_num < min_house:
                    min_house = house_num
    print(min_house)

    houses = [0]*10000000
    min_house = min_presents // 10
    for elf in itertools.count(start=1):
        if elf >= min_house:
            break
        for visited, house_num in enumerate(range(elf, min_house, elf)):
            if visited >= 50:
                break
            houses[house_num] += 11*elf
            if houses[house_num] >= min_presents:
                if house_num < min_house:
                    min_house = house_num
    print(min_house)
