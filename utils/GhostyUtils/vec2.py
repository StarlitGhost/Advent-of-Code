from enum import Enum
from typing import Union, Sequence
import math

VecDataType = Union[int, float]
VecTupleType = Union['_Vec', tuple]


class _Vec:
    # prevent the base class from being instantiated
    def __init__(self):
        if type(self) is _Vec:
            raise TypeError(f"only child classes of '{_Vec.__name__}' may be instantiated")

    @classmethod
    def from_tuple(cls, t: tuple) -> '_Vec':
        return cls(t)

    @classmethod
    def from_str(cls, s: str, split: str = ', ') -> '_Vec':
        return cls(tuple(map(int, s.split(split))))

    def as_tuple(self) -> tuple:
        return tuple(self)

    def __iter__(self) -> VecDataType:
        # for tuple()/list() conversion
        for d in self._data:
            yield d

    def __str__(self) -> str:
        return '('+', '.join(str(d) for d in self._data)+')'

    def __add__(self, other: VecTupleType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__iadd__(other)

    def __radd__(self, other: tuple) -> '_Vec':
        if type(other) is not tuple:
            return NotImplemented
        cls = type(self)
        return cls(other).__iadd__(self)

    def __iadd__(self, other: VecTupleType) -> '_Vec':
        cls = type(self)
        if type(other) is tuple:
            other = cls(other)
        elif type(other) is not cls:
            return NotImplemented

        self._data = list(map(sum, zip(self._data, other._data)))

        self._make_int_if_exact()
        return self

    def __neg__(self) -> '_Vec':
        cls = type(self)
        return cls(tuple(-d for d in self._data))

    def __sub__(self, other: VecTupleType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__isub__(other)

    def __rsub__(self, other: tuple) -> '_Vec':
        if type(other) is not tuple:
            return NotImplemented
        cls = type(self)
        return cls(other).__isub__(self)

    def __isub__(self, other: VecTupleType) -> '_Vec':
        cls = type(self)
        if type(other) is tuple:
            other = cls(other)
        elif type(other) is not cls:
            return NotImplemented

        self += -other

        self._make_int_if_exact()
        return self

    def __mul__(self, other: VecDataType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__imul__(other)

    def __rmul__(self, other: VecDataType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__imul__(other)

    def __imul__(self, other: VecDataType) -> '_Vec':
        if type(other) not in [int, float]:
            return NotImplemented

        self._data = [d * other for d in self._data]

        self._make_int_if_exact()
        return self

    def __truediv__(self, other: VecDataType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__itruediv__(other)

    def __itruediv__(self, other: VecDataType) -> '_Vec':
        if type(other) not in [int, float]:
            return NotImplemented

        self._data = [d / other for d in self._data]

        self._make_int_if_exact()
        return self

    def __floordiv__(self, other: VecDataType) -> '_Vec':
        cls = type(self)
        new = cls(tuple(self))
        return new.__ifloordiv__(other)

    def __ifloordiv__(self, other: VecDataType) -> '_Vec':
        if type(other) not in [int, float]:
            return NotImplemented

        self._data = [d // other for d in self._data]

        self._make_int_if_exact()
        return self

    def __abs__(self) -> VecDataType:
        return self.magnitude()

    def __eq__(self, other: VecTupleType) -> bool:
        cls = type(self)
        if type(other) is tuple:
            other = cls(other)
        if type(other) is cls:
            return self._data == other._data
        else:
            return NotImplemented

    def __ne__(self, other: VecTupleType) -> bool:
        return not self.__eq__(other)

    def __getitem__(self, idx: int) -> VecDataType:
        return self._data[idx]

    def __setitem__(self, idx: int, value: VecDataType) -> None:
        self._data[idx] = value

    def unit(self) -> '_Vec':
        new = self / self.magnitude()
        new._make_int_if_exact()
        return new

    def magnitude(self) -> VecDataType:
        return math.sqrt(sum(d ** 2 for d in self._data))

    def _make_int_if_exact(self) -> None:
        for i, d in enumerate(self._data):
            if type(d) is float and d.is_integer():
                self._data[i] = int(d)

    @classmethod
    def manhattan_distance(cls, start: VecTupleType, end: VecTupleType) -> int:
        if type(start) in [tuple, list]:
            start = cls(tuple(start))
        if type(end) in [tuple, list]:
            end = cls(tuple(end))

        return sum(abs(sd - ed) for sd, ed in zip(start._data, end._data))


class Vec2(_Vec):
    def __init__(self,
                 x: Union[VecDataType, tuple, 'Dir'],
                 y: VecDataType = None) -> None:
        if y is None:
            if type(x) in [tuple, list] and len(x) == 2:
                self._data = list(x)
            elif type(x) is Dir:
                self._data = list(x.value)
            else:
                raise ValueError(f"Couldn't init Vec2 with {x} ({type(x)}), no y given")
        elif type(x) in [int, float] and type(y) in [int, float]:
            self._data = [x, y]
        else:
            raise ValueError(f"Couldn't init Vec2 with {x} ({type(x)}), {y} ({type(y)})")

    @property
    def x(self) -> VecDataType:
        return self._data[0]

    @x.setter
    def x(self, value: VecDataType):
        self._data[0] = value

    @property
    def y(self) -> VecDataType:
        return self._data[1]

    @y.setter
    def y(self, value: VecDataType):
        self._data[1] = value

    def __iadd__(self, other: VecTupleType) -> 'Vec2':
        if type(other) is Dir:
            other = Vec2(other)

        return super().__iadd__(other)

    def __isub__(self, other: VecTupleType) -> 'Vec2':
        if type(other) is Dir:
            other = Vec2(other)

        return super().__isub__(other)

    def north_angle(self) -> float:
        return (math.atan2(self.y, self.x) / math.pi * 180.0 + 90.0) % 360.0


class Dir(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    UP = U = N = NORTH
    DOWN = D = S = SOUTH
    LEFT = L = W = WEST
    RIGHT = R = E = EAST

    NORTH_EAST = NE = (1, -1)
    SOUTH_EAST = SE = (1, 1)
    SOUTH_WEST = SW = (-1, 1)
    NORTH_WEST = NW = (-1, -1)

    def flipped(self) -> 'Dir':
        return Dir(tuple(-Vec2(self)))

    @staticmethod
    def map_udlr(udlr: Sequence) -> 'Dir':
        return {s: d for s, d in zip(udlr, [Dir.UP, Dir.DOWN, Dir.LEFT, Dir.RIGHT])}

    @staticmethod
    def map_nswe(nswe: Sequence) -> 'Dir':
        return {s: d for s, d in zip(nswe, [Dir.NORTH, Dir.SOUTH, Dir.WEST, Dir.EAST])}

    def as_vec2(self) -> Vec2:
        return Vec2(self.value)

    def as_tuple(self) -> tuple:
        return self.value


def manhattan_distance(start: VecTupleType, end: VecTupleType) -> int:
    return Vec2.manhattan_distance(start, end)
