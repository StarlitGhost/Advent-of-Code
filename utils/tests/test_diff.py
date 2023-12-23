from GhostyUtils import diff


def test_hamming_distance():
    assert diff.hamming_distance('#...', '...#') == 2
