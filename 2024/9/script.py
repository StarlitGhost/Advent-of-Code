from GhostyUtils import aoc


def expand_diskmap(diskmap: str) -> list:
    filesystem = []
    for i, c in enumerate(diskmap):
        if i % 2 == 0:  # even, file
            filesystem.extend([i//2]*int(c))
        else:  # odd, free space
            filesystem.extend(['.']*int(c))
    return filesystem


def print_filesystem(filesystem: list):
    print(''.join(str(c) for c in filesystem))


def defrag(filesystem: list) -> list:
    while '.' in filesystem:
        f = filesystem.pop()
        if f == '.':
            continue
        filesystem[filesystem.index('.')] = f

        if aoc.args().verbose:
            print_filesystem(filesystem)
    return filesystem


def checksum(filesystem: list) -> int:
    return sum(pos * id for pos, id in enumerate(filesystem))


def main():
    diskmap = aoc.read()

    filesystem = expand_diskmap(diskmap)

    if aoc.args().verbose:
        print_filesystem(filesystem)

    fs = defrag(filesystem)
    print(f"p1: {checksum(fs)}")


if __name__ == "__main__":
    main()
