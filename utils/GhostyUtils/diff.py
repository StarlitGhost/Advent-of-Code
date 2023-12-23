from collections.abc import Sequence


def hamming_distance(left: Sequence, right: Sequence) -> int:
    """Returns the number of differences between 2 equal-length sequences"""

    if len(left) != len(right):
        raise ValueError('Sequences must be of equal length')

    return sum(l != r for l, r in zip(left, right))
