from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
import curses
import time


class Arcade:
    def __init__(self, use_curses: bool):
        self.cpu = IntCode(aoc.read(), input=self.controls, output=self.draw)

        self.use_curses = use_curses
        if use_curses:
            self._init_curses()
        self.reset()

    def _init_curses(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(True)

    def reset(self):
        self.cpu.reset()
        self.grid = Grid(' ')
        self.input_data = []
        self.score = 0
        self.playing = False

    def process(self):
        self.cpu.process()

    def draw(self, value: int):
        self.input_data.append(value)
        if len(self.input_data) != 3:
            return

        if self.input_data[0] != -1:
            self.draw_tile(tuple(self.input_data))
        else:
            self.score = self.input_data[2]
            self.draw_score()
        self.input_data.clear()

    def draw_tile(self, instr: tuple):
        x, y, tile_idx = instr
        self.grid.expand_for(Vec2(x, y), 0)
        tile = ' #=-o'[tile_idx]
        self.grid[(x, y)] = tile

        if not self.use_curses:
            return

        self.screen.addch(y, x, ord(tile))

        if self.playing:
            self.screen.refresh()
            time.sleep(8 / 1000)
        elif (y, x) == (self.grid.width() - 1, self.grid.height() - 1):
            self.screen.refresh()

    def draw_score(self):
        if not self.use_curses:
            return

        self.screen.addstr(0, 13, f"[ Score: {self.score:5} ]")

    def controls(self) -> int:
        if not self.playing:
            self.playing = True

        ball = Vec2(self.grid.find('o'))
        paddle = Vec2(self.grid.find('-'))
        if paddle.x < ball.x:
            return 1
        elif paddle.x > ball.x:
            return -1
        return 0


def main():
    arcade = Arcade(use_curses=False)

    arcade.process()
    p1 = sum(1 for v in arcade.grid.find_all('='))

    arcade.reset()
    arcade.cpu.memory[0] = 2

    arcade.process()
    if arcade.use_curses:
        curses.endwin()

    print('p1:', p1)
    print('p2:', arcade.score)


if __name__ == "__main__":
    main()
