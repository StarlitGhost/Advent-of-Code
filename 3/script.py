import string


def priority(item):
    if item in string.ascii_lowercase:
        return list(string.ascii_lowercase).index(item) + 1
    else:
        return list(string.ascii_uppercase).index(item) + 27

with open('input') as f:
    inputs = [line.rstrip('\n') for line in f]
    prio_sum = 0

    for line in inputs:
        half_length = len(line)//2
        # print(line, half_length*2)
        l = line[:half_length]
        r = line[half_length:]
        # print(l, r, len(l), len(r))
        item = set(l).intersection(set(r)).pop()
        prio_sum += priority(item)
    print(prio_sum)

    prio_sum = 0

    def chunk(inputs, chunk_size):
        return (inputs[pos:pos + chunk_size] for pos in range(0, len(inputs), chunk_size))

    for elves in chunk(inputs, 3):
        shared_item = set.intersection(*[set(elf) for elf in elves]).pop()
        prio_sum += priority(shared_item)
    print(prio_sum)
