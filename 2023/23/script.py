from GhostyUtils import aoc, pathfinding
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from functools import partial


force_dir = Dir.map_udlr('^v<>')


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
        if travel_dir is forced_dir.flipped():
            return False

    if grid[cur_pos] in force_dir:
        if travel_dir is not force_dir[grid[cur_pos]]:
            return False

    return True


def is_intersection(grid: Grid, pos: tuple):
    neighbours = [grid[n] for n in grid.neighbours(pos, diagonal=False)]
    if neighbours.count('.') > 2:
        return True
    return False


def intersection_bfs(grid: Grid, start, intersections):
    distances = {}

    passable_func = partial(passable, grid=grid, ignore_slopes=True)

    visited = set()
    frontier = [(start, 0)]
    while frontier:
        pos, distance = frontier.pop(0)
        if pos in intersections and pos != start:
            distances[pos] = distance
            continue
        for new_pos in grid.neighbours(pos, diagonal=False, connects=passable_func):
            if new_pos not in visited:
                visited.add(new_pos)
                frontier.append((new_pos, distance + 1))
    return {start: distances}


def reduce_grid(grid: Grid, intersections):
    intersection_distances = {}
    for intersection in intersections:
        distances = intersection_bfs(grid, intersection, intersections)
        intersection_distances.update(distances)
    return intersection_distances


def intersection_dfs(i_distances, start, end):
    frontier = [(start, 0, {start})]
    longest = 0
    while frontier:
        intersection, distance_so_far, visited = frontier.pop()
        if intersection == end:
            longest = max(longest, distance_so_far)
            continue
        for connected, distance in i_distances[intersection].items():
            if connected not in visited:
                connected_distance = distance_so_far + distance
                connected_visited = visited | {connected}
                frontier.append((connected, connected_distance, connected_visited))
    return longest


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())

    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), grid.height()-1)

    passable_func = partial(passable, grid=grid)
    neighbours = partial(grid.neighbours, diagonal=False, connects=passable_func)

    for path in pathfinding.bfs(start, end, all_paths=True, neighbours=neighbours):
        pass

    path_overlay = {pos: 'O' for pos in path}
    print(grid.render_with_overlays([path_overlay]))
    print('p1:', len(path) - 1)

    # replace all the slopes with .
    walkable = set()
    walkable.update(grid.find_all('^'), grid.find_all('v'), grid.find_all('<'), grid.find_all('>'))
    for pos in walkable:
        grid[pos] = '.'
    walkable.update(grid.find_all('.'))

    # find all the intersections, any . with more than 2 . next to it
    intersections = []
    for pos in walkable:
        if is_intersection(grid, pos):
            intersections.append(pos)
    # sort by y position
    intersections.sort(key=lambda p: p[1])

    i_distances = reduce_grid(grid, [start] + intersections + [end])
    longest = intersection_dfs(i_distances, start, end)

    print('p2:', longest)
