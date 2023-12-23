from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from functools import partial


def not_rocks(pos, other_pos, grid: Grid):
    if grid[other_pos] != '#':
        return True
    else:
        return False


def step(grid: Grid, frontier: set[tuple]) -> set[tuple]:
    new_frontier = set()
    connects = partial(not_rocks, grid=grid)
    for pos in frontier:
        neighbours = grid.neighbours(pos, diagonal=False, connects=connects)
        new_frontier.update(neighbours)
    return new_frontier


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())
    start = grid.find('S')
    frontier = set()
    frontier.add(start)

    def plot_overlay(frontier):
        return {f: 'O' for f in frontier}

    print(grid)
    for i in range(64):
        frontier = step(grid, frontier)
        print(f'= {i+1} Steps =')
        print(grid.render_with_overlays([plot_overlay(frontier)]))
    print(len(frontier))
