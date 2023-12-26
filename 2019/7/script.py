from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from collections import deque
import itertools
from typing import Iterable


def init_cpus(memory):
    io = [deque() for _ in range(5)]
    cpus = []
    for cpu in range(1, 6):
        cpus.append(IntCode(memory, input=io[cpu-1].popleft, output=io[cpu % len(io)].append))
    return cpus, io


def find_highest_thrust(cpus: list[IntCode], io: list[deque], phase_range: Iterable[int]):
    max_thrust_signal = 0
    max_phases = []
    for phases in itertools.permutations(phase_range):
        for i, phase in enumerate(phases):
            io[i].append(phase)
            cpus[i].reset()
        io[0].append(0)

        while not all(cpu.halted() for cpu in cpus):
            for cpu in cpus:
                cpu.process()

        thrust_signal = io[0].popleft()
        if thrust_signal > max_thrust_signal:
            max_thrust_signal = thrust_signal
            max_phases = phases
        io[-1].clear()
    return max_thrust_signal, max_phases


def main():
    cpus, io = init_cpus(aoc.read())

    max_thrust, max_phases = find_highest_thrust(cpus, io, range(0, 5))
    print(f'p1: {max_thrust} | {max_phases}')

    max_thrust, max_phases = find_highest_thrust(cpus, io, range(5, 10))
    print(f'p2: {max_thrust} | {max_phases}')


def test():
    programs = [
        {
            'mem_in': "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
            'output': 43210,
            'range': range(0, 5),
        },
        {
            'mem_in': "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,"
                      "1,24,23,23,4,23,99,0,0",
            'output': 54321,
            'range': range(0, 5),
        },
        {
            'mem_in': "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
                      "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            'output': 65210,
            'range': range(0, 5),
        },
        {
            'mem_in': "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
                      "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
            'output': 139629729,
            'range': range(5, 10),
        },
        {
            'mem_in': "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,"
                      "1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,"
                      "1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,"
                      "56,-1,56,1005,56,6,99,0,0,0,0,10",
            'output': 18216,
            'range': range(5, 10),
        }
    ]
    for prog in programs:
        cpus, io = init_cpus(prog['mem_in'])
        max_thrust, max_phases = find_highest_thrust(cpus, io, prog['range'])
        assert max_thrust == prog['output']


if __name__ == "__main__":
    test()
    main()
