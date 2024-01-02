from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from GhostyUtils.vec2 import Vec2, Dir
from GhostyUtils.grid import Grid
from collections import deque, defaultdict


moves = Dir.map_nswe([1, 2, 3, 4])
translate = {v: k for k, v in moves.items()}


class Droid:
    def __init__(self, grid: dict):
        self.cpu = IntCode(aoc.read(), input=self.next_move, output=self.status)
        self.pos = Vec2(0, 0)
        self.grid = grid
        self.last_move = Dir.N
        self.reverse_path = []
        self.search_space = set(self.neighbours())
        self.move_queue = deque([Dir.N])

    def process(self):
        while self.search_space and not self.cpu.halted():
            self.cpu.process()

    def neighbours(self):
        adjacent = [tuple(self.pos + d) for d in [Dir.N, Dir.E, Dir.S, Dir.W]]
        # filter out directions that lead into walls
        adjacent = [pos for pos in adjacent if self.grid[pos] != '#']
        return adjacent

    def next_move(self):
        move = self.move_queue.popleft()
        self.last_move = move
        # print('next move!', move, translate[move])
        return translate[move]

    def status(self, code: int):
        move_pos = tuple(self.pos + self.last_move)

        match code:
            # hit a wall
            case 0:
                self.grid[move_pos] = '#'
            # moved
            case 1:
                if self.grid[move_pos] == '':
                    self.grid[move_pos] = '.'
                    self.reverse_path.append(self.last_move.flipped())
                self.pos = Vec2(move_pos)
            # found oxygen system
            case 2:
                if self.grid[move_pos] == '':
                    self.grid[move_pos] = 'O'
                    self.reverse_path.append(self.last_move.flipped())
                    print('p1:', len(self.reverse_path))
                self.pos = Vec2(move_pos)

        # remove the space we just uncovered from the search space
        if move_pos in self.search_space:
            self.search_space.remove(move_pos)

        neighbours = [n for n in self.neighbours() if self.grid[n] == '']
        if neighbours:
            self.search_space.update(neighbours)
            self.move_queue.append(Dir(tuple(neighbours[0] - self.pos)))
        else:
            # reverse our path until we find unexplored neighbours
            if not self.reverse_path:
                return
            backwards = self.reverse_path.pop()
            self.move_queue.append(backwards)


def bfs(start: tuple, grid: Grid):
    frontier = [[start]]
    visited = set()

    while frontier:
        path = frontier.pop(0)
        pos = path[-1]
        for new_pos in grid.neighbours(pos, diagonal=False):
            if grid[new_pos] == '#' or new_pos in visited:
                continue
            visited.add(new_pos)
            frontier.append(path + [new_pos])

    # the last path to finish will be the longest,
    # and therefore gives us our oxygen spread time
    return path


def main():
    grid = defaultdict(str, {(0, 0): '.'})
    droid = Droid(grid)

    droid.process()

    grid = Grid.from_sparse(grid, ' ')
    start = grid.find('O')
    path = bfs(start, grid)
    print('p2:', len(path) - 1)


if __name__ == "__main__":
    main()
