from GhostyUtils.vec2 import _Vec, VecDataType, Vec2
from typing import Union


class Vec3(_Vec):
    def __init__(self,
                 x: Union[VecDataType, tuple, 'Vec3'],
                 y: VecDataType = None,
                 z: VecDataType = None) -> None:
        if y is None:
            if type(x) in [tuple, list] and len(x) == 3:
                self._data = list(x)
            elif type(x) is Vec3:
                self._data = x._data.copy()
            else:
                raise ValueError(f"Couldn't init {type(self).__name__} with "
                                 f"{x} ({type(x)}), no y or z given")
        elif z is None:
            if type(x) in [int, float] and type(y) in [int, float]:
                self._data = [x, y, 0]
            elif type(x) is Vec2 and type(y) in [int, float]:
                self._data = [x.x, x.y, y]
            else:
                raise ValueError(f"Couldn't init {type(self).__name__} with "
                                 f"{x} ({type(x)}), "
                                 f"{y} ({type(y)}), "
                                 f"no z given (would default to 0)")
        elif type(x) in [int, float] and type(y) in [int, float] and type(z) in [int, float]:
            self._data = [x, y, z]
        else:
            raise ValueError(f"Couldn't init {type(self).__name__} with "
                             f"{x} ({type(x)}), "
                             f"{y} ({type(y)}), "
                             f"{z} ({type(z)})")

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

    @property
    def z(self) -> VecDataType:
        return self._data[2]

    @z.setter
    def z(self, value: VecDataType):
        self._data[2] = value
