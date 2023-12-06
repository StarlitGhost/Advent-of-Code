import sys

class Board:
    def __init__(self, board):
        self._board = [[i for i in row] for row in board]
        self.board = [[[i for i in row] for row in board],
                      [[i for i in row] for row in board]]
        self.width = len(board[0])
        self.height = len(board)
        self.cycle = 0

    def reset(self):
        self.board = [[[i for i in row] for row in self._board],
                      [[i for i in row] for row in self._board]]

    def count_neighbours(self, x, y):
        count = 0

        x_start = x-1 if x > 0 else 0
        x_end = x+1 if x < self.width-1 else self.width-1
        # row above
        if y > 0:
            count += self.board[self.cycle%2][y-1][x_start:x_end+1].count('#')
        # this row
        if x > 0: # not at left edge
            count += 1 if self.board[self.cycle%2][y][x_start] == '#' else 0
        if x < self.width-1: # not at right edge
            count += 1 if self.board[self.cycle%2][y][x_end] == '#' else 0
        # row below
        if y < self.height-1:
            count += self.board[self.cycle%2][y+1][x_start:x_end+1].count('#')
        return count

    def step(self):
        for y, row in enumerate(self.board[self.cycle%2]):
            for x, state in enumerate(row):
                count = self.count_neighbours(x, y)
                if state == '#':
                    self.board[(self.cycle+1)%2][y][x] = '#' if count in [2,3] else '.'
                elif state == '.':
                    self.board[(self.cycle+1)%2][y][x] = '#' if count == 3 else '.'
        self.cycle += 1

    def count_on(self):
        return sum(row.count('#') for row in self.board[self.cycle%2])

    def force_corners(self):
        self.board[self.cycle%2][           0][            0] = '#'
        self.board[self.cycle%2][self.width-1][            0] = '#'
        self.board[self.cycle%2][           0][self.height-1] = '#'
        self.board[self.cycle%2][self.width-1][self.height-1] = '#'

    def __str__(self):
        return '\n'.join([f'step {self.cycle} : {self.count_on()} on',
                          '\n'.join(''.join(row) for row in self.board[self.cycle%2])])


if __name__ == '__main__':
    board = Board([[c for c in line.rstrip('\n')] for line in open(sys.argv[1])])

    #print(board)
    for i in range(100):
        board.step()
        #print(board)
    print(board.count_on())

    board.reset()
    board.force_corners()
    #print(board)
    for i in range(100):
        board.step()
        board.force_corners()
        #print(board)
    print(board.count_on())
