class Vec2:
    def __init__(self, x: int, y: int) -> None:
        self._data = [x, y]

    @property
    def x(self) -> int:
        return self._data[0]

    @x.setter
    def x(self, value: int):
        self._data[0] = value

    @property
    def y(self) -> int:
        return self._data[1]

    @y.setter
    def y(self, value: int):
        self._data[1] = value

    @staticmethod
    def from_tuple(t: tuple) -> 'Vec2':
        return Vec2(*t)

    @staticmethod
    def from_str(self, s: str, split: str = ',') -> 'Vec2':
        return Vec2.from_tuple(*tuple(map(int, s.split(split))))

    def as_tuple(self) -> tuple:
        return tuple(self._data)

    def __str__(self) -> str:
        return ','.join(str(d) for d in self._data)

    def __add__(self, other: 'Vec2') -> 'Vec2':
        new = Vec2(self.x, self.y)
        return new.__iadd__(other)

    def __iadd__(self, other: 'Vec2') -> 'Vec2':
        self.x += other.x
        self.y += other.y
        return self

    def __neg__(self) -> 'Vec2':
        return Vec2(-self.x, -self.y)

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        new = Vec2(self.x, other.x)
        return new.__isub__(other)

    def __isub__(self, other: 'Vec2') -> 'Vec2':
        self.x -= other.x
        self.y -= other.y
        return self

    def __eq__(self, other: 'Vec2') -> bool:
        if type(other) is tuple:
            other = Vec2.from_tuple(other)
        if type(other) is Vec2:
            return self.x == other.x and self.y == other.y
        else:
            raise ValueError(f"Tried to compare Vec2 with {type(other)}")

    def __ne__(self, other: 'Vec2') -> bool:
        return not self.__eq__(other)

    def __getitem__(self, idx: int) -> int:
        return self._data[idx]

    def __setitem__(self, idx: int, value: int) -> None:
        self._data[idx] = value


def manhattan_distance(start: Vec2, end: Vec2) -> int:
    return abs(start.x - end.x) + abs(start.y - end.y)
