from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from collections import deque
import itertools


def init_cpus(memory):
    io = [deque() for _ in range(6)]
    cpus = []
    for cpu in range(1, 6):
        cpus.append(IntCode(memory, input=io[cpu-1].popleft, output=io[cpu].append))
    return cpus, io


def find_highest_thrust(cpus, io):
    max_thrust_signal = 0
    max_phases = []
    for phases in itertools.permutations(range(5)):
        for i, phase in enumerate(phases):
            io[i].append(phase)
            cpus[i].reset()
        io[0].append(0)

        for cpu in cpus:
            cpu.process()

        thrust_signal = io[-1].popleft()
        if thrust_signal > max_thrust_signal:
            max_thrust_signal = thrust_signal
            max_phases = phases
        io[-1].clear()
    return max_thrust_signal, max_phases


def main():
    test()

    cpus, io = init_cpus(aoc.read())

    max_thrust, max_phases = find_highest_thrust(cpus, io)

    print(f'p1: {max_thrust} | {max_phases}')


def test():
    programs = [
        {
            'mem_in': "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
            'output': 43210
        },
        {
            'mem_in': "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            'output': 54321
        },
        {
            'mem_in': "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            'output': 65210
        },
    ]
    for prog in programs:
        cpus, io = init_cpus(prog['mem_in'])
        max_thrust, max_phases = find_highest_thrust(cpus, io)
        assert max_thrust == prog['output']


if __name__ == "__main__":
    main()
