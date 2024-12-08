from collections.abc import Sequence
from typing import Iterable, Any, Callable
import itertools
from GhostyUtils.vec2 import Vec2


class Grid:
    def __init__(self, data: Sequence[str], *, convert: Callable = None) -> None:
        if not convert:
            convert = (lambda v: v)
        self.grid = [[convert(x) for x in row] for row in data]
        self._width = len(self.grid[0])
        self._height = len(self.grid)

    @staticmethod
    def from_sparse(data: dict[tuple, Any], empty: Any = None) -> 'Grid':
        tl = Vec2(min(data.keys(), key=lambda k: k[0])[0],
                  min(data.keys(), key=lambda k: k[1])[1])
        br = Vec2(max(data.keys(), key=lambda k: k[0])[0],
                  max(data.keys(), key=lambda k: k[1])[1])
        width = br.x - tl.x + 1
        height = br.y - tl.y + 1
        grid_list = []
        for y in range(height):
            grid_list.append([])
            for x in range(width):
                coord = (x + tl.x, y + tl.y)
                value = data[coord] if coord in data else empty
                grid_list[y].append(value)
        grid = Grid(grid_list)
        grid._offset = tl
        return grid

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def find(self, target: str) -> tuple:
        for y, row in enumerate(self.grid):
            for x, element in enumerate(row):
                if element == target:
                    return (x, y)

    def find_all(self, target: str) -> Iterable[tuple]:
        for y, row in enumerate(self.grid):
            for x, element in enumerate(row):
                if element == target:
                    yield (x, y)

    def expand_for(self, pos: Vec2, fill: str = None):
        if pos.x >= self._width:
            for row in self.grid:
                row.extend(fill for _ in range(pos.x + 1 - self._width))
            self._width = pos.x + 1
        if pos.y >= self._height:
            self.grid.extend([fill for _ in range(self._width)]
                             for _ in range(pos.y + 1 - self._height))
            self._height = pos.y + 1

    def by_rows(self, *, reverse: bool = False) -> Iterable[Sequence]:
        for row in (self.grid if not reverse else reversed(self.grid)):
            yield row

    def by_cols(self, *, reverse: bool = False) -> Iterable[Sequence]:
        # getting rid of this list() call would be good if possible,
        # to avoid duplicating the whole grid in memory
        for col in (zip(*self.grid) if not reverse else reversed(list(zip(*self.grid)))):
            yield col

    def by_cell(self) -> Iterable[tuple[Any, tuple]]:
        for y, row in enumerate(self.grid):
            for x, element in enumerate(row):
                yield element, (x, y)

    def transposed(self) -> 'Grid':
        return Grid(list(zip(*self.grid)))

    def vec2_inside(self, position: Vec2) -> bool:
        """deprecated, use .in_bounds()"""
        return self.in_bounds(position)

    def in_bounds(self, position: Vec2) -> bool:
        if type(position) is tuple:
            position = Vec2(position)
        return ((0 <= position.x < self._width) and
                (0 <= position.y < self._height))

    def neighbours(self, position: Vec2, *, diagonal: bool = True, connects: Callable = None):
        if type(position) is tuple:
            position = Vec2(position)
        x, y = position.as_tuple()
        if diagonal:
            coords = [(x+dx, y+dy)
                      for dx, dy in
                      itertools.product([-1, 0, 1], repeat=2)
                      if not dx == dy == 0]
        else:
            coords = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        coords = [c for c in coords if self.in_bounds(c)]
        if connects:
            coords = [c for c in coords if connects(position, c)]
        return coords

    def __str__(self):
        return '\n'.join(''.join(str(o) for o in row) for row in self.grid)

    def render_with_overlays(self, overlays: list[dict[tuple, Any]]) -> str:
        def overlay(obj, pos):
            s = None
            for o in reversed(overlays):
                if pos in o and s is None:
                    s = str(o[pos])
                    break
            if s is None:
                s = str(obj)
            return s

        return '\n'.join(''.join(overlay(o, (x, y)) for x, o in enumerate(row))
                         for y, row in enumerate(self.grid))

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
