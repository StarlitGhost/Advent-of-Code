from GhostyUtils import aoc
import itertools


def validate(password, reject_large_groups=False):
    pw = str(password)
    if not all(int(l) <= int(r) for l, r in zip(pw, pw[1:])):
        return False
    if not any(l == r for l, r in zip(pw, pw[1:])):
        return False
    if reject_large_groups:
        if not any(len(list(g)) == 2 for k, g in itertools.groupby(pw)):
            return False
    return True


def main():
    MIN, MAX = map(int, aoc.read().split('-'))
    passwords = [pw for pw in range(MIN, MAX) if validate(pw)]
    print('p1:', len(passwords))

    passwords = [pw for pw in range(MIN, MAX) if validate(pw, True)]
    print('p2:', len(passwords))


if __name__ == "__main__":
    main()
