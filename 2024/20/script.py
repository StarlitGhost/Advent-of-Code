from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, manhattan_distance as mh_dist
from GhostyUtils.pathfinding import bfs
from collections import defaultdict
from functools import partial


aoc.argparser.add_argument("-s", "--save", type=int, default=100, help="picoseconds to save")


# non-walls 1 space UDLR from pos
def neighbours(pos: tuple, grid: Grid) -> list[tuple]:
    return [n for n in grid.neighbours(pos, diagonal=False) if grid[n] != '#']


# non-walls behind walls, 2 spaces UDLR from pos
def cheat(pos: tuple, grid: Grid) -> list[Vec2]:
    pos = Vec2(pos)

    def end_pos(pos, n):
        return pos+(n-pos)*2

    return [end_pos(pos, n) for n in grid.neighbours(pos, diagonal=False)
            if grid[n] == '#' and grid.in_bounds(end_pos(pos, n)) and grid[end_pos(pos, n)] != '#']


def cheat_savings(saves: dict[int], minimum: int):
    for saving, cheats in sorted(list(saves.items())):
        if saving < minimum:
            continue
        print(f"There are {cheats} cheats that save {saving} picoseconds.")


def main():
    racetrack = Grid(aoc.read_lines())
    start = racetrack.find('S')
    end = racetrack.find('E')
    target = aoc.args.save

    neighbours_func = partial(neighbours, grid=racetrack)
    clean_path = next(bfs(start, end, neighbours=neighbours_func))
    clean_time = len(clean_path)
    # map clean path positions to their index in the list, for faster lookup
    clean_path_index = {pos: i for i, pos in enumerate(clean_path)}

    # print the clean path
    if aoc.args.progress or aoc.args.verbose:
        overlays = [
            {path: '.' for path in clean_path},
            {start: 'S', end: 'E'},
        ]
        print(racetrack.render_with_overlays(overlays))
        print(f"clean time: {clean_time} picoseconds")

    saves = defaultdict(int)
    cheats = {}
    for i, pos in enumerate(clean_path[:-1]):
        for c in cheat(pos, racetrack):
            # skip cheats that take us backwards
            if clean_path_index[c.as_tuple()] < i:
                continue

            # calculate the time saved
            saved = -(i - clean_path_index[c.as_tuple()] + 2)
            saves[saved] += 1
            cheats[(pos, c.as_tuple())] = saved

            # draw the cheats on the map
            if aoc.args.verbose:
                overlays.append({(pos+(c-pos)/2).as_tuple(): '1',
                                 c.as_tuple(): '2'})
                print(racetrack.render_with_overlays(overlays))
                print(f"^ saves {saved} picoseconds")
                overlays.pop()

    if aoc.args.progress or aoc.args.verbose:
        cheat_savings(saves, target)
    print(f"p1: {sum(times for saved, times in saves.items() if saved >= 100)}")

    saves = defaultdict(int)
    for i, pos in enumerate(clean_path[:-target]):
        # loop over path positions that are over 100 positions forward along the path and under
        # 20 manhattan distance away from the current position
        for candidate, md in filter(lambda md: md[1] <= 20,
                                    ((other, mh_dist(pos, other))
                                     for other in clean_path[i+target:])):
            # calculate the time saved
            saved = -(i - clean_path_index[candidate] + md)
            saves[saved] += 1

    if aoc.args.progress or aoc.args.verbose:
        cheat_savings(saves, target)
    print(f"p2: {sum(times for saved, times in saves.items() if saved >= target)}")


if __name__ == "__main__":
    main()
