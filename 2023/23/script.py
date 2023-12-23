from GhostyUtils import aoc, pathfinding
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from functools import partial


force_dir = {
    '^': Dir.UP,
    'v': Dir.DOWN,
    '<': Dir.LEFT,
    '>': Dir.RIGHT,
}


def passable(current_pos, next_pos, *, grid: Grid, ignore_slopes: bool = False):
    cur_pos = Vec2(*current_pos)
    next_pos = Vec2(*next_pos)

    if grid[next_pos] == '#':
        return False

    if ignore_slopes:
        return True

    travel_dir = Dir(tuple(next_pos - cur_pos))
    if grid[next_pos] in force_dir:
        forced_dir = force_dir[grid[next_pos]]
        if travel_dir is Dir(tuple(-Vec2(forced_dir))):
            return False

    if grid[cur_pos] in force_dir:
        if travel_dir is not force_dir[grid[cur_pos]]:
            return False

    return True


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())

    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), grid.height()-1)

    passable_func = partial(passable, grid=grid)
    neighbours = partial(grid.neighbours, diagonal=False, connects=passable_func)

    paths = pathfinding.bfs(start, end, all_paths=True, neighbours=neighbours)

    paths.sort(key=lambda p: len(p))
    path_overlay = {pos: 'O' for pos in paths[-1]}
    print(grid.render_with_overlays([path_overlay]))
    print('p1:', len(paths[-1]) - 1)

    passable_func = partial(passable, grid=grid, ignore_slopes=True)
    neighbours = partial(grid.neighbours, diagonal=False, connects=passable_func)

    paths = pathfinding.bfs(start, end, all_paths=True, neighbours=neighbours)

    paths.sort(key=lambda p: len(p))
    path_overlay = {pos: 'O' for pos in paths[-1]}
    print(grid.render_with_overlays([path_overlay]))
    print('p2:', len(paths[-1]) - 1)
