from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
from itertools import combinations


# calculates and returns a list of antinode positions from a pair of antenna
def calc_antinodes(a: tuple, b: tuple, grid: Grid, resonates: bool = False) -> list[tuple]:
    a, b = Vec2(a), Vec2(b)
    v = b - a  # vector between a & b
    # print(f"a: {a} b: {b} v: {v} | {a - v} {b + v}")

    nodes = []

    # p1
    if not resonates:
        aa = (a - v).as_tuple()  # project v back from a
        ab = (b + v).as_tuple()  # project v forward from b
        nodes += [aa] if grid.in_bounds(aa) else []
        nodes += [ab] if grid.in_bounds(ab) else []

    # p2
    else:
        # add the antenna positions themselves
        nodes += [a.as_tuple(), b.as_tuple()]

        # repeatedly project v back from a until we go out of bounds
        pos = a - v
        while grid.in_bounds(pos):
            nodes += [pos.as_tuple()]
            pos -= v

        # repeatedly project v forward from b until we go out of bounds
        pos = b + v
        while grid.in_bounds(pos):
            nodes += [pos.as_tuple()]
            pos += v

    return nodes


def main():
    grid = Grid(aoc.read_lines())
    antennas = {}

    # find all the antennas, and store them as {frequency: [positions]}
    for freq, pos in grid.by_cell():
        if freq != '.':
            antennas.setdefault(freq, []).append(pos)

    antinode_positions = set()

    # calculate antinodes for each antenna frequency
    for antenna, positions in antennas.items():
        for combo in combinations(positions, 2):
            antinode_positions.update(calc_antinodes(*combo, grid))
    if aoc.args().verbose:
        print(grid.render_with_overlays([{pos: '#' for pos in antinode_positions},
                                         {p: freq for freq, pos in antennas.items() for p in pos}]))
    print(f"p1: {len(antinode_positions)}")

    # calculate antinodes for each antenna frequency, with resonance
    for antenna, positions in antennas.items():
        for combo in combinations(positions, 2):
            antinode_positions.update(calc_antinodes(*combo, grid, resonates=True))
    if aoc.args().verbose:
        print(grid.render_with_overlays([{pos: '#' for pos in antinode_positions},
                                         {p: freq for freq, pos in antennas.items() for p in pos}]))
    print(f"p2: {len(antinode_positions)}")


if __name__ == "__main__":
    main()
