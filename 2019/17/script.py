from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
import math


class Video:
    def __init__(self):
        self.str_frame = []
        self.frame = None

    def input(self, v: int):
        # part 2 we get a large value when the robot stops
        if v > 255:
            print('p2:', v)

        self.str_frame.append(chr(v))
        if self.str_frame[-2:] == ['\n', '\n']:
            # skipping the final \n\n with the [:-2]
            frame = ''.join(px for px in self.str_frame[:-2])
            self.frame = Grid(frame.split('\n'))
            # print(self.frame)


def build_path(grid: Grid):
    start = grid.find('^')
    path = [(start, Dir.UP)]
    while True:
        cur_pos, move_dir = path[-1]
        cur_pos = Vec2(cur_pos)

        # try forward first
        next_pos = tuple(cur_pos + move_dir)
        if grid.in_bounds(next_pos) and grid[next_pos] == '#':
            path.append((next_pos, move_dir))
            continue

        # try left
        next_pos = tuple(cur_pos + move_dir.turn_left())
        if grid.in_bounds(next_pos) and grid[next_pos] == '#':
            path.append((next_pos, move_dir.turn_left()))
            continue

        # try right
        next_pos = tuple(cur_pos + move_dir.turn_right())
        if grid.in_bounds(next_pos) and grid[next_pos] == '#':
            path.append((next_pos, move_dir.turn_right()))
            continue

        # no more valid moves, we've reached the end
        moves = []
        for first, second in zip(path, path[1:]):
            if first[1].turn_left() == second[1]:
                moves.append('L')
            if first[1].turn_right() == second[1]:
                moves.append('R')
            if type(moves[-1]) is int:
                moves[-1] += 1
            else:
                moves.append(1)
        return ','.join(str(m) for m in moves)


class Controls:
    def __init__(self, grid: Grid):
        # path = build_path(grid)
        # print(path)
        # R,12,L,6,R,12,L,8,L,6,L,10,R,12,L,6,R,12,R,12,L,10,L,6,R,10,L,8,L,6,L,10,R,12,L,10,L,6,R,10,L,8,L,6,L,10,R,12,L,10,L,6,R,10,R,12,L,6,R,12,R,12,L,10,L,6,R,10

        # controls created by vim's / pattern highlighting of above!
        self.controls = (
            'A,B,A,C,B,C,B,C,A,C\n'
            'R,12,L,6,R,12\n'
            'L,8,L,6,L,10\n'
            'R,12,L,10,L,6,R,10\n'
            'n\n'
        )
        self.iter = iter(self.controls)

    def __call__(self):
        return ord(next(self.iter))


def main():
    video = Video()
    cpu = IntCode(aoc.read(), output=video.input)
    cpu.process()

    scaffolds = video.frame.find_all('#')
    alignment_sum = 0
    for scaf in scaffolds:
        if all(video.frame[n] == '#' for n in video.frame.neighbours(scaf, diagonal=False)):
            alignment_sum += math.prod(scaf)
    print('p1:', alignment_sum)

    cpu = IntCode(aoc.read(), input=Controls(video.frame), output=video.input)
    cpu.memory[0] = 2
    cpu.process()


if __name__ == "__main__":
    main()
