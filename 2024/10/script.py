from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.pathfinding import bfs
import functools


def passable(current_pos, next_pos, *, grid: Grid):
    if grid[next_pos] == grid[current_pos] + 1:
        return True
    return False


def max_height(current_pos, *, grid: Grid):
    return grid[current_pos] == 9


def main():
    grid = Grid(aoc.read_lines(), convert=int)
    if aoc.args.verbose:
        print(grid)

    passable_func = functools.partial(passable, grid=grid)
    neighbours = functools.partial(grid.neighbours, diagonal=False, connects=passable_func)
    early_out = functools.partial(max_height, grid=grid)

    total_score = 0
    total_rating = 0
    for trailhead in grid.find_all(0):
        ends = set()
        for path in bfs(start=trailhead, end=None, all_paths=True,
                        neighbours=neighbours, early_out=early_out):
            ends.add(path[-1])
            total_rating += 1
        total_score += len(ends)

    print(f"p1: {total_score}")
    print(f"p2: {total_rating}")


if __name__ == "__main__":
    main()
