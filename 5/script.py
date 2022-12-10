import string


def chunk(inputs, chunk_size):
    return (inputs[pos:pos + chunk_size] for pos in range(0, len(inputs), chunk_size))


def read_stacks(inputs):
    stacks = {}
    for line in inputs:
        for idx, crate in enumerate(chunk(line, 4)):
            if not ''.join(crate).strip():
                continue

            if crate[1] in string.digits:
                for key in stacks.keys():
                    stacks[key].reverse()
                return stacks

            stack = idx+1
            #print(''.join(crate[0:]), stack)

            if stack not in stacks:
                stacks[stack] = []
            stacks[stack].append(crate[1])
        #print(stacks)


def process_move(move, stacks):
    _, num, _, from_, _, to = move.split()
    for crate in range(0, int(num)):
        stacks[int(to)].append(stacks[int(from_)].pop())


with open('input') as f:
    inputs = (line.rstrip('\n') for line in f)

    stacks = read_stacks(inputs)
    #print(stacks)

    for move in inputs:
        if move.strip():
            process_move(move, stacks)
    #print(stacks)
    top_crates = [stacks[crate][-1] for crate in range(1,9+1)]
    print(''.join(top_crates))
