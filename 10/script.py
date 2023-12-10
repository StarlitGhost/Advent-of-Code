import sys
from enum import Enum

class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

dir_offset = {Dir.WEST: (-1,0),
              Dir.EAST: (1,0),
              Dir.NORTH: (0,-1),
              Dir.SOUTH: (0,1)}

pipe_connects = {'|': [Dir.NORTH, Dir.SOUTH],
                 '-': [Dir.EAST, Dir.WEST],
                 'L': [Dir.NORTH, Dir.EAST],
                 'J': [Dir.NORTH, Dir.WEST],
                 '7': [Dir.SOUTH, Dir.WEST],
                 'F': [Dir.SOUTH, Dir.EAST],
                 '.': [],
                 'S': [Dir.NORTH, Dir.SOUTH, Dir.EAST, Dir.WEST]}

dir_connects = {Dir.NORTH: Dir.SOUTH,
                Dir.SOUTH: Dir.NORTH,
                Dir.EAST: Dir.WEST,
                Dir.WEST: Dir.EAST}


if __name__ == '__main__':
    rows = open(sys.argv[1]).read().strip().split('\n')
    pipe_grid = [[x for x in row] for row in rows]
    sy = [y for y, row in enumerate(pipe_grid) if 'S' in row][0]
    sx = pipe_grid[sy].index('S')
    s_pos = (sx, sy)

    def grid(pos, offset=(0,0)):
        return pipe_grid[pos[1]+offset[1]][pos[0]+offset[0]]

    def move(pos, offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    pos = s_pos
    path = [s_pos]
    came_from = None
    done = False
    while not done:
        # filter out the direction we came from, we can't go backwards
        search_dirs = [dir_ for dir_ in pipe_connects[grid(pos)] if dir_ != came_from]
        for dir_ in search_dirs:
            # get the pipe in the direction we're searching
            pipe = grid(pos, dir_offset[dir_])
            # if it's S, we're done
            if pipe == 'S':
                done = True
                break
            # if the pipe we're looking at connects to our current position, move to that pipe
            if dir_connects[dir_] in pipe_connects[pipe]:
                pos = move(pos, dir_offset[dir_])
                path.append(pos)
                came_from = dir_connects[dir_]
                break

    print(len(path) // 2)
