from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from collections import defaultdict


def area(region: list[Vec2]) -> int:
    return len(region)


def neighbours(pos: Vec2) -> list[Vec2]:
    return [
        (pos + Vec2(Dir.UP)).as_tuple(),
        (pos + Vec2(Dir.DOWN)).as_tuple(),
        (pos + Vec2(Dir.LEFT)).as_tuple(),
        (pos + Vec2(Dir.RIGHT)).as_tuple(),
    ]


def perimeter(region: set[tuple]) -> int:
    # for each position in the region,
    # count how many of its neighbours are outside the region
    return sum(n not in region for pos in region for n in neighbours(pos))


def sides(region: set[tuple]) -> int:
    # gather fences by the direction they are facing
    fences = defaultdict(list)
    for pos in region:
        for n, d in Dir.map_nswe(neighbours(pos)).items():
            # no same-region neighbour in this direction, we found a fence
            if n not in region:
                fences[d].append(pos)

    # sort fences by y coord if facing north/south, or x coord for east/west
    for d, fs in fences.items():
        fences[d] = sorted(fs, key=lambda f: f[::-1] if d in {Dir.N, Dir.S} else f)

    # calculate the number of distinct sides facing each direction
    num_sides = 0
    dirmap = {
        Dir.N: Dir.E,
        Dir.S: Dir.E,
        Dir.W: Dir.S,
        Dir.E: Dir.S,
    }
    for d, fs in fences.items():
        num_sides += 1
        for f1, f2 in zip(fs, fs[1:]):
            # if two fences in the list aren't directly next to each other,
            # we found a new side
            if (Vec2(f1) + dirmap[d]).as_tuple() != f2:
                num_sides += 1

    return num_sides


def main():
    grid = Grid(aoc.read_lines())
    regions = []
    checked = set()
    for region, pos in grid.by_cell():
        if pos in checked:
            continue

        regions.append(grid.bfs_flood_find(pos, search=region))
        checked.update(regions[-1])

    if aoc.args.progress or aoc.args.verbose:
        for region in regions:
            r = grid[next(iter(region))]
            print(f"{r} | "
                  f"area: {area(region)}, "
                  f"perimeter: {perimeter(region)}, "
                  f"sides: {sides(region)} | "
                  f"p1 cost: {area(region) * perimeter(region)} | "
                  f"p2 cost: {area(region) * sides(region)}")
            if aoc.args.verbose:
                print(f"> {region}")
        print(f"{len(regions)} regions")

    print(f"p1: {sum(area(region) * perimeter(region) for region in regions)}")
    print(f"p2: {sum(area(region) * sides(region) for region in regions)}")


if __name__ == "__main__":
    main()
