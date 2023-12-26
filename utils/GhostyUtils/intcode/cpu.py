from typing import Union, Iterable, Callable
from enum import Enum


class PMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class IntCode:
    def __init__(self,
                 memory: Union[list[int], str] = None,
                 input: Callable = None,
                 output: Callable = None):
        if memory is None:
            self.memory = []
        else:
            self.load_memory(memory)
        self._init_memory = list(self.memory)
        self.i_ptr = 0

        if input is None:
            self.input = [].pop
        else:
            self.input = input

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

    def set_input_func(self, input_func: Callable):
        self.input = input_func

    def set_output_func(self, output_func: Callable):
        self.output = output_func

    def halted(self) -> bool:
        return self.memory[self.i_ptr] == 99

    def process(self) -> list[int]:
        while True:
            instr = self.memory[self.i_ptr]
            modes = IntCode.modes(instr)
            instr = instr % 100

            match instr:
                case 99:  # halt
                    # self.i_ptr += 1
                    return
                case 1:  # add
                    self.i_ptr += self._add(self.i_ptr+1, modes)
                case 2:  # mul
                    self.i_ptr += self._mul(self.i_ptr+1, modes)
                case 3:  # input
                    try:
                        self.i_ptr += self._input(self.i_ptr+1, modes)
                    except IndexError:
                        return
                case 4:  # output
                    self.i_ptr += self._output(self.i_ptr+1, modes)
                case 5:  # jump-if-true
                    self.i_ptr = self._jump_if_true(self.i_ptr+1, modes)
                case 6:  # jump-if-false
                    self.i_ptr = self._jump_if_false(self.i_ptr+1, modes)
                case 7:  # less than
                    self.i_ptr += self._less_than(self.i_ptr+1, modes)
                case 8:  # equals
                    self.i_ptr += self._equals(self.i_ptr+1, modes)
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
        self.i_ptr = 0

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

        self.memory[store] = self.input()

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
