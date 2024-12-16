from GhostyUtils import aoc, pathfinding
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from functools import partial


def neighbours(pos: tuple[tuple[int], Dir], maze: Grid):
    pos, dir = pos
    return [(n, (Vec2(n) - Vec2(pos)).as_tuple())
            for n in filter(lambda p: maze[p] != '#', maze.neighbours(pos, diagonal=False))]


def cost(current: tuple[tuple[int], Dir], next_: tuple[tuple[int], Dir]):
    _, c_dir = current
    _, n_dir = next_

    if c_dir == n_dir:
        return 1
    elif Dir(n_dir) in {Dir(c_dir).turn_left(), Dir(c_dir).turn_right()}:
        return 1000 + 1
    else:
        return 2001


def heuristic(next_pos: tuple[tuple[int], Dir], end: tuple[int]) -> int:
    next_pos, _ = next_pos
    return Vec2.manhattan_distance(next_pos, end)


def early_out(current, end):
    return current[0] == end


def main():
    maze = Grid(aoc.read_lines())
    start = (maze.find('S'), Dir.EAST.as_tuple())
    end = maze.find('E')

    neighbours_func = partial(neighbours, maze=maze)
    early_out_func = partial(early_out, end=end)
    came_from, cost_so_far, last_pos = pathfinding.a_star(start, end,
                                                          neighbours=neighbours_func,
                                                          cost=cost,
                                                          heuristic=heuristic,
                                                          early_out=early_out_func)
    path = pathfinding.reconstruct_path(came_from, start, last_pos)

    if aoc.args.progress or aoc.args.verbose:
        path_overlay = {pos: {Dir.N: '^', Dir.S: 'v', Dir.E: '>', Dir.W: '<'}[Dir(dir)]
                        for pos, dir in path}
        print(maze.render_with_overlays([path_overlay]))
    print(f"p1: {cost_so_far[last_pos]}")


if __name__ == "__main__":
    main()
