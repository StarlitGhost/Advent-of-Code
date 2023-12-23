from GhostyUtils import aoc


def process(memory):
    i_ptr = 0
    while True:
        instr = memory[i_ptr]

        match instr:
            case 99:  # halt
                i_ptr += 1
                return memory
            case 1:  # add
                i_ptr += add(i_ptr+1, memory)
            case 2:  # mul
                i_ptr += mul(i_ptr+1, memory)


def add(addr: int, memory: list[int]) -> int:
    l, r, store = memory[addr:addr+3]
    memory[store] = memory[l] + memory[r]
    return 4


def mul(addr: int, memory: list[int]) -> int:
    l, r, store = memory[addr:addr+3]
    memory[store] = memory[l] * memory[r]
    return 4


def read_memory(memory: str) -> list[int]:
    return list(map(int, memory.split(',')))


def str_memory(memory):
    return ','.join(str(i) for i in memory)


def test():
    programs = [
        [[1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70,2,3,11,0,99,30,40,50]],  # noqa: E231
        [[1,0,0,0,99], [2,0,0,0,99]],  # noqa: E231
        [[2,3,0,3,99], [2,3,0,6,99]],  # noqa: E231
        [[2,4,4,5,99,0], [2,4,4,5,99,9801]],  # noqa: E231
        [[1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]],  # noqa: E231
    ]
    for prog in programs:
        assert process(prog[0]) == prog[1]
    return True


if __name__ == "__main__":
    test()

    orig_memory = read_memory(aoc.read())

    memory = orig_memory.copy()
    memory[1] = 12
    memory[2] = 2
    memory = process(memory)
    print(memory[0])

    for noun in range(100):
        for verb in range(100):
            memory = orig_memory.copy()
            memory[1] = noun
            memory[2] = verb
            if process(memory)[0] == 19690720:
                print(100 * noun + verb)
                break
