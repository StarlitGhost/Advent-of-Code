from GhostyUtils import aoc
from dataclasses import dataclass


@dataclass
class Block:
    id: str
    size: int


def expand_diskmap(diskmap: str) -> list:
    filesystem = []
    for pos, length in enumerate(diskmap):
        if pos % 2 == 0:  # even, file
            filesystem.append(Block(pos//2, int(length)))
        else:  # odd, free space
            filesystem.append(Block('.', int(length)))
    return filesystem


def print_filesystem(filesystem: list):
    print(''.join(str(block.id) * block.size for block in filesystem))


def frag(filesystem: list) -> list:
    if aoc.args().verbose or aoc.args().progress:
        print("# frag")

    new_fs = []
    # grab a data block from the end of the filesystem
    working_block = filesystem.pop()
    free_block = Block('.', 0)

    while filesystem:
        # grab a block from the start of the filesystem
        block = filesystem.pop(0)

        # data block, just add it
        if block.id != '.':
            if block.size != 0:
                new_fs.append(block)

        # free space block
        else:
            # frag data blocks at the end of the filesystem to fill this free space
            while block.size > 0:
                # skip over free space blocks at the end of the filesystem
                if working_block.id == '.':
                    free_block.size += working_block.size
                    working_block = filesystem.pop()

                # take a chunk of data that will fit in this free space block
                chunk = min(working_block.size, block.size)
                new_fs.append(Block(working_block.id, chunk))
                # reduce the size of the data block by the size of the chunk we took
                working_block.size -= chunk
                # reduce the size of this free space block
                block.size -= chunk
                # increase the size of the free space block at the end of the filesystem
                free_block.size += chunk
                # grab a new data block if we used up the current one
                if working_block.size <= 0:
                    working_block = filesystem.pop()

        if aoc.args().verbose:
            print_filesystem(new_fs + filesystem + [working_block, free_block])

    # add any leftover chunks of blocks
    if block.id != '.' and block.size > 0:
        new_fs.append(block)
    if working_block.id != '.' and working_block.size > 0:
        new_fs.append(working_block)

    # add all the free space back at the end of the filesystem
    new_fs.append(free_block)

    return new_fs


def compact(filesystem: list) -> list:
    if aoc.args().verbose or aoc.args().progress:
        print("# compact")

    new_fs = filesystem.copy()

    if aoc.args().verbose:
        print_filesystem(new_fs)

    for block in reversed(filesystem):
        if block.id == '.':
            continue
        cur_index = new_fs.index(block)

        # find a large enough block of free space left of the current block
        for index, check_block in enumerate(new_fs[:cur_index]):
            # skip files and blocks of free space that aren't large enough
            if check_block.id != '.' or check_block.size < block.size:
                continue

            # reduce the free space block by the size of the block we're moving
            new_fs[index].size -= block.size
            # insert a free space block where the block we're moving came from
            #  note: I was surprised this worked, I thought I'd have to merge
            #        the new free space with any free space around it;
            #        each block only getting one shot at a right-to-left move
            #        means it doesn't come up
            new_fs.insert(cur_index, Block('.', block.size))
            # remove the block we're moving from its old position
            new_fs.remove(block)
            # insert the block we're moving at its new position
            new_fs.insert(index, block)

            if aoc.args().verbose:
                print_filesystem(new_fs)

            break

    return new_fs


def checksum(filesystem: list) -> int:
    pos = 0
    total = 0
    for block in filesystem:
        # skip over free space
        if block.id == '.':
            pos += block.size
            continue

        for i in range(block.size):
            total += (pos + i) * int(block.id)
        pos += block.size

    return total


def main():
    diskmap = aoc.read()

    filesystem = expand_diskmap(diskmap)

    if aoc.args().progress:
        print_filesystem(filesystem)

    fs = frag(filesystem)
    if aoc.args().progress:
        print_filesystem(fs)
    print(f"p1: {checksum(fs)}")

    filesystem = expand_diskmap(diskmap)
    fs = compact(filesystem)
    if aoc.args().progress:
        print_filesystem(fs)
    print(f"p2: {checksum(fs)}")


if __name__ == "__main__":
    main()
