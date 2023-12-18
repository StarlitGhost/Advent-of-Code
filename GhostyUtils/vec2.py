from enum import Enum
from typing import Union


Vec2DataType = Union[int, float]
Vec2TupleType = Union['Vec2', tuple]


class Vec2:
    def __init__(self,
                 x: Union[Vec2DataType, tuple, 'Dir'],
                 y: Vec2DataType = None) -> None:
        if y is None:
            if type(x) is tuple and len(x) == 2:
                self._data = list(x)
            elif type(x) is Dir:
                self._data = x.value
            else:
                raise ValueError(f"Couldn't init Vec2 with {x} ({type(x)}), no y given")
        elif type(x) in [int, float] and type(y) in [int, float]:
            self._data = [x, y]
        else:
            raise ValueError(f"Couldn't init Vec2 with {x} ({type(x)}), {y} ({type(y)})")

    @property
    def x(self) -> Vec2DataType:
        return self._data[0]

    @x.setter
    def x(self, value: Vec2DataType):
        self._data[0] = value

    @property
    def y(self) -> Vec2DataType:
        return self._data[1]

    @y.setter
    def y(self, value: Vec2DataType):
        self._data[1] = value

    @staticmethod
    def from_tuple(t: tuple) -> 'Vec2':
        return Vec2(*t)

    @staticmethod
    def from_str(self, s: str, split: str = ',') -> 'Vec2':
        return Vec2.from_tuple(*tuple(map(int, s.split(split))))

    def as_tuple(self) -> tuple:
        return tuple(self)

    def __iter__(self) -> Vec2DataType:
        # for tuple()/list() conversion
        for d in self._data:
            yield d

    def __str__(self) -> str:
        return '('+','.join(str(d) for d in self._data)+')'

    def __add__(self, other: Vec2TupleType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__iadd__(other)

    def __radd__(self, other: tuple) -> 'Vec2':
        if type(other) is not tuple:
            return NotImplemented
        return Vec2.from_tuple(other).__iadd__(self)

    def __iadd__(self, other: Vec2TupleType) -> 'Vec2':
        if type(other) is tuple:
            other = Vec2.from_tuple(other)
        elif type(other) is Dir:
            other = Vec2(other)
        elif type(other) is not Vec2:
            return NotImplemented

        self.x += other.x
        self.y += other.y
        return self

    def __neg__(self) -> 'Vec2':
        return Vec2(-self.x, -self.y)

    def __sub__(self, other: Vec2TupleType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__isub__(other)

    def __rsub__(self, other: tuple) -> 'Vec2':
        if type(other) is not tuple:
            return NotImplemented
        return Vec2.from_tuple(other).__isub__(self)

    def __isub__(self, other: Vec2TupleType) -> 'Vec2':
        if type(other) is tuple:
            other = Vec2.from_tuple(other)
        elif type(other) is Dir:
            other = Vec2(other)
        elif type(other) is not Vec2:
            return NotImplemented

        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2DataType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__imul__(other)

    def __rmul__(self, other: Vec2DataType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__imul__(other)

    def __imul__(self, other: Vec2DataType) -> 'Vec2':
        if type(other) not in [int, float]:
            return NotImplemented

        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other: Vec2DataType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__itruediv__(other)

    def __itruediv__(self, other: Vec2DataType) -> 'Vec2':
        if type(other) not in [int, float]:
            return NotImplemented

        self.x /= other
        self.y /= other
        return self

    def __floordiv__(self, other: Vec2DataType) -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__ifloordiv__(other)

    def __ifloordiv__(self, other: Vec2DataType) -> 'Vec2':
        if type(other) not in [int, float]:
            return NotImplemented

        self.x //= other
        self.y //= other
        return self

    def __eq__(self, other: Vec2TupleType) -> bool:
        if type(other) is tuple:
            other = Vec2.from_tuple(other)
        if type(other) is Vec2:
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __ne__(self, other: Vec2TupleType) -> bool:
        return not self.__eq__(other)

    def __getitem__(self, idx: int) -> Vec2DataType:
        return self._data[idx]

    def __setitem__(self, idx: int, value: Vec2DataType) -> None:
        self._data[idx] = value


class Dir(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    UP = NORTH
    DOWN = SOUTH
    LEFT = WEST
    RIGHT = EAST

    def as_vec2(self) -> Vec2:
        return Vec2.from_tuple(self.value)

    def as_tuple(self) -> tuple:
        return self.value


def manhattan_distance(start: Vec2TupleType, end: Vec2TupleType) -> int:
    if type(start) is tuple:
        start = Vec2(start)
    if type(end) is tuple:
        end = Vec2(end)

    return abs(start.x - end.x) + abs(start.y - end.y)
