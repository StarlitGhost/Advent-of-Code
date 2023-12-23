from GhostyUtils import aoc
import itertools
from math import prod
import sys


def package_groups(packages, target_weight):
    min_size = sys.maxsize
    for group_size in range(1, len(packages)):
        if min_size < group_size:
            break
        for combo in itertools.combinations(packages, group_size):
            if sum(combo) == target_weight:
                min_size = group_size
                yield combo


def qe(group):
    return prod(group)


if __name__ == "__main__":
    packages = tuple(map(int, aoc.read_lines()))
    total_weight = sum(packages)

    lowest_qe = sys.maxsize
    for g in package_groups(packages, total_weight // 3):
        g_qe = qe(g)
        if g_qe < lowest_qe:
            lowest_qe = g_qe
    print(lowest_qe)

    lowest_qe = sys.maxsize
    for g in package_groups(packages, total_weight // 4):
        g_qe = qe(g)
        if g_qe < lowest_qe:
            lowest_qe = g_qe
    print(lowest_qe)
