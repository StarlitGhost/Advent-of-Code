from GhostyUtils.vec2 import Vec2, Dir, manhattan_distance


def test_init():
    # test tuple instantiation
    assert Vec2((7, 8)) == Vec2(7, 8)


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


def test_dir():
    assert Dir.UP is Dir.NORTH and Dir.UP == Dir.NORTH
    assert Dir.UP is not Dir.SOUTH
    assert Dir.NORTH.value == (0, -1) == Vec2(0, -1) == Vec2(Dir.NORTH)


def test_manhattan_distance():
    assert manhattan_distance(Vec2(2, 7), Vec2(10, 4)) == 11
    assert manhattan_distance((2, 7), (10, 4)) == 11
