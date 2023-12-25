from typing import Union, Iterable, Callable
from enum import Enum


class PMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class IntCode:
    def __init__(self,
                 memory: Union[list[int], str] = None,
                 input_gen: Iterable[int] = None,
                 output: Callable = None):
        if memory is None:
            self.memory = []
        else:
            self.load_memory(memory)
        self._init_memory = list(self.memory)

        if input_gen is None:
            self.input = (_ for _ in [])
        else:
            self.input = input_gen

        if output is None:
            self.output = (lambda _: {}["attempted to write to non-existent output"])
        else:
            self.output = output

    def load_memory(self, memory: Union[list[int], str]):
        if type(memory) is str:
            self.memory = list(map(int, memory.split(',')))
        elif type(memory) is list:
            self.memory = memory
        else:
            raise ValueError(f"cannot load IntCode memory with {type(memory)}")

    def str_memory(self) -> str:
        return ','.join(str(i) for i in self.memory)

    def process(self) -> list[int]:
        i_ptr = 0
        while True:
            instr = self.memory[i_ptr]
            modes = IntCode.modes(instr)
            instr = instr % 100

            match instr:
                case 99:  # halt
                    i_ptr += 1
                    return self.memory
                case 1:  # add
                    i_ptr += self._add(i_ptr+1, modes)
                case 2:  # mul
                    i_ptr += self._mul(i_ptr+1, modes)
                case 3:  # input
                    i_ptr += self._input(i_ptr+1, modes)
                case 4:  # output
                    i_ptr += self._output(i_ptr+1, modes)
                case 5:  # jump-if-true
                    i_ptr = self._jump_if_true(i_ptr+1, modes)
                case 6:  # jump-if-false
                    i_ptr = self._jump_if_false(i_ptr+1, modes)
                case 7:  # less than
                    i_ptr += self._less_than(i_ptr+1, modes)
                case 8:  # equals
                    i_ptr += self._equals(i_ptr+1, modes)
                case _:
                    raise ValueError(f"unrecognized instruction {instr}")

    @staticmethod
    def modes(instr: int) -> Iterable[PMode]:
        instr //= 100
        while instr != 0:
            yield PMode(instr % 10)
            instr //= 10
        while True:
            yield PMode.POSITION

    def reset(self):
        self.memory = list(self._init_memory)

    def _load(self, addr: int, mode: PMode) -> int:
        if mode is PMode.POSITION:
            return self.memory[self.memory[addr]]
        elif mode is PMode.IMMEDIATE:
            return self.memory[addr]

    # opcode 1 : add
    def _add(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._load(addr, next(modes))
        r = self._load(addr+1, next(modes))
        store = self.memory[addr+2]

        self.memory[store] = l + r

        return 4

    # opcode 2 : mul
    def _mul(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._load(addr, next(modes))
        r = self._load(addr+1, next(modes))
        store = self.memory[addr+2]

        self.memory[store] = l * r

        return 4

    # opcode 3 : input
    def _input(self, addr: int, modes: Iterable[PMode]) -> int:
        store = self.memory[addr]

        self.memory[store] = next(self.input)

        return 2

    # opcode 4 : output
    def _output(self, addr: int, modes: Iterable[PMode]) -> int:
        value = self._load(addr, next(modes))

        self.output(value)

        return 2

    # opcode 5 : jump-if-true
    def _jump_if_true(self, addr: int, modes: Iterable[PMode]) -> int:
        cmp = self._load(addr, next(modes))
        i_ptr = self._load(addr+1, next(modes))

        if cmp != 0:
            return i_ptr

        # addr is i_ptr+1, and we have 2 parameters
        return addr+2

    # opcode 6 : jump-if-false
    def _jump_if_false(self, addr: int, modes: Iterable[PMode]) -> int:
        cmp = self._load(addr, next(modes))
        i_ptr = self._load(addr+1, next(modes))

        if cmp == 0:
            return i_ptr

        # addr is i_ptr+1, and we have 2 parameters
        return addr+2

    # opcode 7 : less than
    def _less_than(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._load(addr, next(modes))
        r = self._load(addr+1, next(modes))
        store = self.memory[addr+2]

        self.memory[store] = 1 if l < r else 0

        return 4

    # opcode 8 : equals
    def _equals(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._load(addr, next(modes))
        r = self._load(addr+1, next(modes))
        store = self.memory[addr+2]

        self.memory[store] = 1 if l == r else 0

        return 4
