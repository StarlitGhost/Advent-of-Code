from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
from itertools import combinations
import math


def antinodes(a: tuple, b: tuple, grid: Grid, resonates: bool = False) -> list[tuple]:
    a, b = Vec2(a), Vec2(b)
    v = b - a
    # print(f"a: {a} b: {b} v: {v} | {a - v} {b + v}")
    nodes = []
    if not resonates:
        aa = (a - v).as_tuple()
        ab = (b + v).as_tuple()
        nodes += [aa] if grid.in_bounds(aa) else []
        nodes += [ab] if grid.in_bounds(ab) else []
    else:
        nodes += [a.as_tuple(), b.as_tuple()]
        pos = a - v
        while grid.in_bounds(pos):
            nodes += [pos.as_tuple()]
            pos -= v
        pos = b + v
        while grid.in_bounds(pos):
            nodes += [pos.as_tuple()]
            pos += v
    return nodes


def main():
    grid = Grid(aoc.read_lines())
    antennas = {}

    for element, pos in grid.by_cell():
        if element != '.':
            antennas.setdefault(element, []).append(pos)

    antinode_positions = set()
    for antenna, positions in antennas.items():
        for combo in combinations(positions, 2):
            antinode_positions.update(antinodes(*combo, grid))

    print(f"p1: {len(antinode_positions)}")

    for antenna, positions in antennas.items():
        for combo in combinations(positions, 2):
            antinode_positions.update(antinodes(*combo, grid, resonates=True))
    print(f"p2: {len(antinode_positions)}")


if __name__ == "__main__":
    main()
