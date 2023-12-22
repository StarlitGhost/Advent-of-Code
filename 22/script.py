from GhostyUtils import aoc
import itertools
from string import ascii_uppercase


def add(t1: tuple, t2: tuple):
    return tuple(map(sum, zip(t1, t2)))


def iter_labels():
    for size in itertools.count(1):
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)


def fall(grid: dict, brick: tuple[tuple, tuple], label: str) -> set[str]:
    x_footprint = abs(brick[0][0] - brick[1][0])
    y_footprint = abs(brick[0][1] - brick[1][1])
    if x_footprint >= 1:
        scan_dir = (1, 0, 0)
    elif y_footprint >= 1:
        scan_dir = (0, 1, 0)
    else:
        scan_dir = (0, 0, 1)
    min_z = min(brick[0][2], brick[1][2])
    start = min(brick[0], brick[1])
    end = max(brick[0], brick[1])
    scan = start
    offset = (0, 0, -min_z+1)
    supports = set()
    while scan != add(end, scan_dir):
        for z in range(1, min_z):
            scan_z = add(scan, (0, 0, -z))
            if scan_z in grid:
                if (0, 0, -z+1) >= offset:
                    offset = (0, 0, -z+1)
                break
        if scan_dir == (0, 0, 1):
            break
        scan = add(scan, scan_dir)
    rest_start = add(start, offset)
    rest_end = add(end, offset)
    rest = rest_start
    while rest != add(rest_end, scan_dir):
        below = add(rest, (0, 0, -1))
        if below in grid and grid[below] != label:
#           print(label, 'sits on', grid[below])
            supports.add(grid[below])
        grid[rest] = label
        rest = add(rest, scan_dir)
    return supports


if __name__ == "__main__":
    grid = {}
    bricks_txt = aoc.read_lines()
    bricks = []
    labels = iter_labels()
    for i, b in enumerate(bricks_txt):
        start, end = b.split('~')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        bricks.append((start, end))
    bricks.sort(key=lambda b: min(b[0][2], b[1][2]))
    sitting_on = {}
    for brick in bricks:
        label = next(labels)
        sitting_on[label] = fall(grid, brick, label)
#   print(sitting_on)
    safe = set(brick for brick in sitting_on)
    for brick, below in sitting_on.items():
        if len(below) == 1 and next(iter(below)) in safe:
            safe.remove(*below)
#   print(safe)
    print('p1:', len(safe))
