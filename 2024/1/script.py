from GhostyUtils import aoc
from collections import Counter


def main():
    inputs = aoc.read_lines()

    left, right = [], []

    for line in inputs:
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))

    distances = [abs(l-r) for l, r in zip(sorted(left), sorted(right))]
    print("p1:", sum(distances))

    rightCounts = Counter(right)
    similarity = [l * rightCounts[l] for l in left]
    print("p2:", sum(similarity))


if __name__ == "__main__":
    main()
