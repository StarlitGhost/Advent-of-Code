from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
from GhostyUtils.pathfinding import a_star, reconstruct_path
from functools import partial


aoc.argparser.add_argument("-s", "--size", type=int, default=71, help="size of 2d memory")
aoc.argparser.add_argument("-b", "--bytes", type=int, default=1024, help="number of bytes to drop")


def neighbours(pos: tuple, grid: Grid) -> list[tuple]:
    return list(cell for cell in grid.neighbours(pos, diagonal=False)
                if grid[cell] != '#')


def main():
    inputs = aoc.read_lines()

    memory = Grid(["."])
    memory.expand_for(Vec2(aoc.args.size-1, aoc.args.size-1), fill='.')

    bytes_ = list(Vec2.from_str(line, split=',') for line in inputs)
    num_bytes = min(len(bytes_), aoc.args.bytes)
    for byte in bytes_[:num_bytes]:
        memory[byte] = '#'

    start = (0, 0)
    end = (memory.width()-1, memory.height()-1)

    neighbour_func = partial(neighbours, grid=memory)
    came_from, _, _ = a_star(start, end, neighbours=neighbour_func)
    path = reconstruct_path(came_from, start, end)

    if aoc.args.verbose or aoc.args.progress:
        overlays = [{pos: 'O' for pos in path},
                    {start: 'S', end: 'E'},]
        print(memory.render_with_overlays(overlays))
    print(f"p1: {len(path)-1}")

    for byte in bytes_[num_bytes:]:
        memory[byte] = '#'
        came_from, _, _ = a_star(start, end, neighbours=neighbour_func)
        path = reconstruct_path(came_from, start, end)
        if len(path) == 0:
            print(f"p2: {byte[0]},{byte[1]}")
            break


if __name__ == "__main__":
    main()
