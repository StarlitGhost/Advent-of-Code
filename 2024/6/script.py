from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


def move(pos: tuple, dir_: Dir, grid: Grid) -> tuple[tuple, Dir]:
    next_pos = pos + Vec2(dir_)

    # out of bounds or open, return next position
    if not grid.in_bounds(next_pos) or not grid[next_pos] in '#O':
        return next_pos.as_tuple(), dir_

    # obstacle, rotate right 90 degrees
    else:
        return pos, dir_.turn_right()


def simulate(pos: tuple, dir_: Dir, grid: Grid) -> tuple[set, list, bool]:
    visited = set()
    visited.add(pos)
    path = []
    path.append((pos, dir_))
    path_set = set()
    path_set.add((pos, dir_))
    loops = False

    while grid.in_bounds(pos):
        pos, dir_ = move(pos, dir_, grid)
        visited.add(pos)
        # we changed direction
        if path[-1][0] == pos:
            path.append((pos, dir_))
            path.append((pos, None))
            path_set.add((pos, dir_))
        # we're following a previous path, loop found
        elif (pos, dir_) in path_set:
            loops = True
            break
        # we just moved forward
        else:
            path.append((pos, dir_))
            path_set.add((pos, dir_))

    return visited, path, loops


def print_path(grid: Grid, path: list, start_pos: tuple):
    dir_chars = {
        Dir.UP: '|',
        Dir.DOWN: '|',
        Dir.LEFT: '-',
        Dir.RIGHT: '-',
        None: '+',
    }
    print(grid.render_with_overlays([{pos: dir_chars[dir_] for pos, dir_ in path},
                                     {start_pos: '^'}]))


def main():
    grid = Grid(aoc.read_lines())

    start_pos = grid.find('^')
    dir_ = Dir.UP

    visited, path, _ = simulate(start_pos, dir_, grid)

    if aoc.args().verbose:
        print(grid.render_with_overlays([{pos: 'X' for pos in visited}]))
        print("p1:", len(visited) - 1)

    loop_obstacles = set()
    tried_obstacles = set()
    path = [p for p in path if p[1] is not None]

    # try placing an obstacle at every position along our initial path
    for i, pair in enumerate(path):
        pos = pair[0]

        # skip the start position, out-of-bounds, and previously tried obstacles
        if pos == start_pos or not grid.in_bounds(pos) or pos in tried_obstacles:
            continue

        # place the obstacle
        grid[pos] = 'O'
        tried_obstacles.add(pos)

        # start pathing from just before the newly placed obstacle
        new_start_pos, new_dir = path[i-1] if path[i-1][0] != pos else path[i-2]

        new_visited, new_path, loops = simulate(new_start_pos, new_dir, grid)

        # track obstacles that cause loops
        if loops:
            loop_obstacles.add(pos)
            if aoc.args().verbose:
                print_path(grid, new_path, new_start_pos)
            if aoc.args().progress or aoc.args().verbose:
                print(f"{i}/{len(path)} {len(loop_obstacles)}")

        # remove the current obstacle so we can try the next one
        grid[pos] = '.'

    if not aoc.args().verbose:
        print("p1:", len(visited) - 1)
    print("p2:", len(loop_obstacles))


if __name__ == "__main__":
    main()
