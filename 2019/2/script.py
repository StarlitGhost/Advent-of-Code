from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode


if __name__ == "__main__":
    cpu = IntCode(aoc.read())
    cpu.memory[1] = 12
    cpu.memory[2] = 2
    cpu.process()
    print('p1:', cpu.memory[0])

    for noun in range(100):
        for verb in range(100):
            cpu.reset()
            cpu.memory[1] = noun
            cpu.memory[2] = verb
            cpu.process()
            if cpu.memory[0] == 19690720:
                print('p2:', 100 * noun + verb)
                break
