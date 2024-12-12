from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


def area(region: list[Vec2]) -> int:
    return len(region)


def neighbours(pos: Vec2) -> list[Vec2]:
    return [
        (pos + Vec2(Dir.UP)).as_tuple(),
        (pos + Vec2(Dir.RIGHT)).as_tuple(),
        (pos + Vec2(Dir.DOWN)).as_tuple(),
        (pos + Vec2(Dir.LEFT)).as_tuple(),
    ]


def perimeter(region: list[Vec2]) -> int:
    p = 0
    for pos in region:
        p += sum(1 for n in neighbours(pos) if n not in region)
    return p


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
            print(f"{r} | area: {area(region)}, perimeter: {perimeter(region)}, "
                  f"cost: {area(region) * perimeter(region)}")
            if aoc.args.verbose:
                print(f"> {region}")
        print(f"{len(regions)} regions")

    print(f"p1: {sum(area(region) * perimeter(region) for region in regions)}")


if __name__ == "__main__":
    main()
