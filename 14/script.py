from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


class RollingRock:
    def __init__(self, pos: Vec2):
        self.pos = pos

    def __str__(self):
        return "O"

    def roll(self, direction: Dir, grid: Grid):
        moveDir = direction.as_vec2()
        offset = self.pos

        # search ahead until we find an obstacle
        while True:
            if not grid.vec2_inside(offset + moveDir):
                break
            ahead = grid[offset + moveDir]
            if ahead == '.':
                offset = offset + moveDir
            else:
                break

        # move to the last open space we found
        grid[self.pos] = '.'
        self.pos = offset
        grid[self.pos] = self


class StaticRock:
    def __init__(self, pos: Vec2):
        self.pos = pos

    def __str__(self):
        return "#"


def tilt(grid: Grid, direction: Dir):
    match direction:
        case Dir.NORTH:
            gridScan = grid.by_rows()
        case Dir.SOUTH:
            gridScan = grid.by_rows(reverse=True)
        case Dir.WEST:
            gridScan = grid.by_cols()
        case Dir.EAST:
            gridScan = grid.by_cols(reverse=True)

    # roll rocks line by line, from the edge tilted down to the opposite side
    for line in gridScan:
        rocks = (rock for rock in line if type(rock) is RollingRock)
        for rock in rocks:
            rock.roll(direction, grid)


def north_load(rocks, height):
    return sum(height - rock[1] for rock in rocks)


def spin(cycle, grid, rocks, history):
    for d, dir_ in enumerate(cycle):
        tilt(grid, dir_)
        new_rock_positions = rock_positions(rocks)
        if new_rock_positions in history:
            return d, history.index(new_rock_positions)
        else:
            history.append(new_rock_positions)
    return 3, -1


def rock_positions(rocks):
    return set(rock.pos.as_tuple() for rock in rocks)


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())
    rocks = []

    for pos in grid.find_all('O'):
        grid[pos] = RollingRock(pos)
        rocks.append(grid[pos])
    for pos in grid.find_all('#'):
        grid[pos] = StaticRock(pos)

    history = [rock_positions(rocks)]

    tilt(grid, Dir.NORTH)
    print('P1 Load:', north_load(rock_positions(rocks), grid.height()))

    history.append(rock_positions(rocks))

    cycle = [Dir.NORTH, Dir.WEST, Dir.SOUTH, Dir.EAST]
    spin(cycle[1:], grid, rocks, history)
    total_spins = 1000000000
    for i in range(1, total_spins):
        loop, end = spin(cycle, grid, rocks, history)
        if end >= 0:
            start_c = end
            end_c = len(history)
            length_c = end_c - start_c
            start_s = start_c / len(cycle)
            end_s = end_c / len(cycle)
            length_s = end_s - start_s
            offset_s = (total_spins - start_s) % length_s
            offset_c = int(offset_s * len(cycle))
            print(f'Start cycle: {start_c} | '
                  f'End cycle: {end_c} | '
                  f'Cycle length: {length_c}')
            print(f'Start spin: {start_s} | '
                  f'End spin: {end_s} | '
                  f'Spin length: {length_s} | '
                  f'Spin offset: {offset_s}')
            print(f'Cycle history offset at {total_spins} spins: '
                  f'{start_c + offset_c}')
            final_rocks = history[start_c + offset_c]
            print('P2 Load:', north_load(final_rocks, grid.height()))
            break
