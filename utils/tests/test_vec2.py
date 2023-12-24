import pytest
from GhostyUtils.vec2 import Vec2, Dir


def test_init():
    # test tuple instantiation
    assert Vec2((7, 8)) == Vec2(7, 8)
    assert Vec2.from_tuple((7, 8)) == Vec2(7, 8)
    with pytest.raises(ValueError):
        Vec2.from_tuple((1, 2, 3))
    with pytest.raises(ValueError):
        Vec2.from_tuple((1,))


def test_iter():
    result = tuple(Vec2(7, 8))
    assert type(result) is tuple and result == (7, 8)

    result = list(Vec2(7, 8))
    assert type(result) is list and result == [7, 8]


def test_add():
    assert Vec2(2, 7) + Vec2(-4, 11) == Vec2(-2, 18)
    assert Vec2(2, 7) + (-4, 11) == Vec2(-2, 18)


def test_radd():
    result = (10, 4) + Vec2(2, 7)
    assert result == Vec2(12, 11)
    assert type(result) is Vec2


def test_sub():
    assert Vec2(2, 7) - Vec2(-4, 11) == Vec2(6, -4)
    assert Vec2(2, 7) - (-4, 11) == Vec2(6, -4)


def test_rsub():
    result = (10, 4) - Vec2(2, 7)
    assert result == Vec2(8, -3)
    assert type(result) is Vec2


def test_neg():
    assert -Vec2(2, 7) == Vec2(-2, -7)


def test_mul():
    assert Vec2(1, 5) * 2 == Vec2(2, 10)
    assert Vec2(1, 5) * -2 == Vec2(-2, -10)


def test_truediv():
    assert Vec2(1, 5) / 2 == Vec2(0.5, 2.5)
    assert Vec2(1, 5) / -2 == Vec2(-0.5, -2.5)


def test_floordiv():
    assert Vec2(1, 5) // 2 == Vec2(0, 2)
    assert Vec2(1, 5) // -2 == Vec2(-1, -3)


def test_magnitude():
    assert abs(Vec2(2, 1.5)) == 2.5


def test_unit():
    assert Vec2(2, 1.5).unit() == Vec2(0.8, 0.6)
    assert abs(Vec2(98, -34).unit()) == 1.0


def test_dir():
    assert Dir.UP is Dir.NORTH and Dir.UP == Dir.NORTH
    assert Dir.UP is not Dir.SOUTH
    assert Dir.NORTH.value == (0, -1) == Vec2(0, -1) == Vec2(Dir.NORTH)
    assert Dir.map_udlr('^v<>') == {
        '^': Dir.UP,
        'v': Dir.DOWN,
        '<': Dir.LEFT,
        '>': Dir.RIGHT,
    }
    assert Dir.map_nswe('NSWE') == {
        'N': Dir.NORTH,
        'S': Dir.SOUTH,
        'W': Dir.WEST,
        'E': Dir.EAST,
    }
    assert Dir.UP.flipped() == Dir.DOWN == Dir.SOUTH
    assert Dir.LEFT.flipped() == Dir.RIGHT == Dir.EAST


def test_dir_vec2():
    assert Vec2(10, 10) + Dir.UP == Vec2(10, 9)
    assert Vec2(10, 10) - Dir.UP == Vec2(10, 11)


def test_manhattan_distance():
    assert Vec2.manhattan_distance(Vec2(2, 7), Vec2(10, 4)) == 11
    assert Vec2.manhattan_distance((2, 7), (10, 4)) == 11
