from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


if __name__ == "__main__":
    cpu = IntCode(aoc.read())
    cpu.memory[1] = 12
    cpu.memory[2] = 2
    out_mem = cpu.process()
    print('p1:', out_mem[0])

    for noun in range(100):
        for verb in range(100):
            cpu.load_memory(aoc.read())
            cpu.memory[1] = noun
            cpu.memory[2] = verb
            if cpu.process()[0] == 19690720:
                print('p2:', 100 * noun + verb)
                break
