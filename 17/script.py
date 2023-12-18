from GhostyUtils import aoc, pathfinding
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir, manhattan_distance
import functools


def heat_cost(cur_pos, next_pos, grid: Grid):
    # calculate cost over the whole distance between cur_pos and next_pos
    d = next_pos[1]
    pos = Vec2(cur_pos[0])
    end = Vec2(next_pos[0])
    cost = 0
    while pos != end:
        pos += d
        cost += grid[pos]
    return cost


def possible_moves(cur_pos, grid: Grid, min_dist=1, max_dist=3):
    dirs_allowed = {
        Dir.UP.as_tuple(): (Dir.LEFT.as_tuple(), Dir.RIGHT.as_tuple()),
        Dir.DOWN.as_tuple(): (Dir.LEFT.as_tuple(), Dir.RIGHT.as_tuple()),
        Dir.LEFT.as_tuple(): (Dir.UP.as_tuple(), Dir.DOWN.as_tuple()),
        Dir.RIGHT.as_tuple(): (Dir.UP.as_tuple(), Dir.DOWN.as_tuple()),
        None: (Dir.UP.as_tuple(), Dir.DOWN.as_tuple(), Dir.LEFT.as_tuple(), Dir.RIGHT.as_tuple())
    }
    moves = []
    dir_ = cur_pos[1] if len(cur_pos) > 1 else None
    for d in dirs_allowed[dir_]:
        for dist in range(min_dist, max_dist+1):
            pos = (Vec2(cur_pos[0]) + Vec2(d) * dist).as_tuple()
            if grid.in_bounds(pos):
                moves.append((pos, d))
    return moves
    # add different travel distances to the list, and
    # add travel directions to each position tuple.
    # something like
    # [((x+1, y), (1, 0)),
    #  ((x+2, y), (1, 0)),
    #  ((x+3, y), (1, 0))]
    # also, use the previous turn directions (in cur_pos)
    # to restrict the move directions generated.


def heuristic(next_pos, end):
    return manhattan_distance(next_pos[0], end)


def reached_end(cur_pos, end):
    return cur_pos[0] == end


def build_overlay(came_from, start, last_pos):
    path = pathfinding.reconstruct_path(came_from, start, last_pos)
    dir_chars = {(0, 1): 'v', (0, -1): '^', (1, 0): '>', (-1, 0): '<'}
    path_overlay = {p[0]: dir_chars[n[1]] for p, n in zip(path, path[1:])}
    return path_overlay


if __name__ == "__main__":
    grid = Grid(aoc.read_lines(), convert=int)

    start = ((0, 0),)
    end = (grid.width()-1, grid.height()-1)

    neighbours = functools.partial(possible_moves, grid=grid)
    cost = functools.partial(heat_cost, grid=grid)
    early_out = functools.partial(reached_end, end=end)
    a_star = functools.partial(pathfinding.a_star,
                               neighbours=neighbours,
                               cost=cost,
                               heuristic=heuristic,
                               early_out=early_out)

    came_from, cost_so_far, last_pos = a_star(start, end)
    #path_overlay = build_overlay(came_from, start, last_pos)
    #print(grid.render_with_overlays([path_overlay]))
    print(cost_so_far[last_pos])

    neighbours = functools.partial(possible_moves, grid=grid, min_dist=4, max_dist=10)
    a_star = functools.partial(pathfinding.a_star,
                               neighbours=neighbours,
                               cost=cost,
                               heuristic=heuristic,
                               early_out=early_out)
    came_from, cost_so_far, last_pos = a_star(start, end)
    #path_overlay = build_overlay(came_from, start, last_pos)
    #print(grid.render_with_overlays([path_overlay]))
    print(cost_so_far[last_pos])
