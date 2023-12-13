from collections.abc import Sequence
from typing import Iterable, Any, Callable
from GhostyUtils.vec2 import Vec2


class Grid:
    def __init__(self, data: Sequence[str]) -> None:
        self.grid = [[x for x in row] for row in data]
        self._width = len(self.grid[0])
        self._height = len(self.grid)

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def find(self, target: str) -> Vec2:
        for y, row in enumerate(self.grid):
            for x, element in enumerate(row):
                if element == target:
                    return Vec2(x, y)

    def find_all(self, target: str) -> Iterable[Vec2]:
        for y, row in enumerate(self.grid):
            for x, element in enumerate(row):
                if element == target:
                    yield Vec2(x, y)

    def by_rows(self) -> Iterable[Sequence]:
        for row in self.grid:
            yield row

    def by_cols(self) -> Iterable[Sequence]:
        for col in zip(*self.grid):
            yield col

    def transposed(self) -> 'Grid':
        return Grid(list(zip(*self.grid)))

    def vec2_inside(self, position: Vec2) -> bool:
        return ((0 <= position.x < self._width) and
                (0 <= position.y < self._height))

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __getitem__(self, key) -> Any:
        if type(key) in [Vec2, tuple]:
            # return the element
            return self.grid[key[1]][key[0]]
        if type(key) in [int, slice]:
            # return the row
            return self.grid[key]
        raise ValueError(f"Tried to get grid item via {type(key)}")

    def __setitem__(self, key, value):
        if type(key) not in [Vec2, tuple]:
            raise ValueError(f"Cannot set grid elements via {type(key)}")
        self.grid[key[1]][key[0]] = value

    def flood_fill(self, pos: Vec2, fill: Any, inside: Callable) -> None:
        """combined-scan-and-fill span filler"""
        """from https://en.wikipedia.org/wiki/Flood_fill#Span_filling"""
        if not inside(Vec2.from_tuple(pos)):
            return
        s = [(pos[0], pos[0], pos[1], 1), (pos[0], pos[0], pos[1] - 1, -1)]
        while s:
            x1, x2, y, dy = s.pop(0)
            x = x1
            if inside(Vec2(x, y)):
                while inside(Vec2(x - 1, y)):
                    self[x-1, y] = fill
                    x -= 1
                if x < x1:
                    s.append((x, x1 - 1, y - dy, -dy))
            while x1 <= x2:
                while inside(Vec2(x1, y)):
                    self[x1, y] = fill
                    x1 += 1
                if x1 > x:
                    s.append((x, x1 - 1, y + dy, dy))
                if x1 - 1 > x2:
                    s.append((x2 + 1, x1 - 1, y - dy, -dy))
                x1 += 1
                while x1 < x2 and not inside(Vec2(x1, y)):
                    x1 += 1
                x = x1
