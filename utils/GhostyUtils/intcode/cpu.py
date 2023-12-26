from typing import Union, Iterable, Callable
from enum import Enum


class PMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class IntCode:
    def __init__(self,
                 memory: Union[list[int], str] = None,
                 input: Callable = None,
                 output: Callable = None):
        if memory is None:
            self.memory = []
            self._init_memory = []
        else:
            self.load_memory(memory)
        
        self.reset()

        if input is None:
            self.input = [].pop
        else:
            self.input = input

        if output is None:
            self.output = (lambda _: {}["attempted to write to non-existent output"])
        else:
            self.output = output

    def reset(self):
        self.memory = list(self._init_memory)
        self.sparse_memory = {}
        self.i_ptr = 0
        self.relative_base = 0

    def load_memory(self, memory: Union[list[int], str]):
        if type(memory) is str:
            self.memory = list(map(int, memory.split(',')))
        elif type(memory) is list:
            self.memory = memory
        else:
            raise ValueError(f"cannot load IntCode memory with {type(memory)}")

        self._init_memory = list(self.memory)
        self.sparse_memory = {}

    def str_memory(self) -> str:
        return ','.join(str(i) for i in self.memory)

    def set_input_func(self, input_func: Callable):
        self.input = input_func

    def set_output_func(self, output_func: Callable):
        self.output = output_func

    def halted(self) -> bool:
        return self._read(self.i_ptr, PMode.IMMEDIATE) == 99

    def process(self) -> list[int]:
        while True:
            instr = self._read(self.i_ptr, PMode.IMMEDIATE)
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
                case 9:  # relative base offset
                    self.i_ptr += self._rel_base_offset(self.i_ptr+1, modes)
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

    def _read(self, addr: int, mode: PMode) -> int:
        if mode is PMode.POSITION:
            mapped_addr = self.memory[addr]
        elif mode is PMode.IMMEDIATE:
            mapped_addr = addr
        elif mode is PMode.RELATIVE:
            mapped_addr = self.relative_base + self.memory[addr]

        if mapped_addr < 0:
            raise IndexError(f"Attempted to read from out-of-bound address"
                             f"{addr}, {mode.name} mode")

        if mapped_addr >= len(self.memory):
            if mapped_addr in self.sparse_memory:
                return self.sparse_memory[mapped_addr]
            else:
                return 0
        else:
            return self.memory[mapped_addr]

    def _write(self, addr: int, mode: PMode, value: int):
        if mode is PMode.POSITION:
            mapped_addr = self.memory[addr]
        elif mode is PMode.IMMEDIATE:
            raise Exception("Immediate mode is not allowed for writes")
        elif mode is PMode.RELATIVE:
            mapped_addr = self.relative_base + self.memory[addr]

        if mapped_addr < 0:
            raise IndexError(f"Attempted to write {value} to out-of-bounds address {addr}")
        if mapped_addr >= len(self.memory):
            self.sparse_memory[mapped_addr] = value
        else:
            self.memory[mapped_addr] = value

    # opcode 1 : add
    def _add(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._read(addr, next(modes))
        r = self._read(addr+1, next(modes))

        out = l + r

        self._write(addr+2, next(modes), out)
        return 4

    # opcode 2 : mul
    def _mul(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._read(addr, next(modes))
        r = self._read(addr+1, next(modes))

        out = l * r

        self._write(addr+2, next(modes), out)
        return 4

    # opcode 3 : input
    def _input(self, addr: int, modes: Iterable[PMode]) -> int:
        out = self.input()

        self._write(addr, next(modes), out)
        return 2

    # opcode 4 : output
    def _output(self, addr: int, modes: Iterable[PMode]) -> int:
        value = self._read(addr, next(modes))

        self.output(value)

        return 2

    # opcode 5 : jump-if-true
    def _jump_if_true(self, addr: int, modes: Iterable[PMode]) -> int:
        cmp = self._read(addr, next(modes))
        i_ptr = self._read(addr+1, next(modes))

        if cmp != 0:
            return i_ptr

        # addr is i_ptr+1, and we have 2 parameters
        return addr+2

    # opcode 6 : jump-if-false
    def _jump_if_false(self, addr: int, modes: Iterable[PMode]) -> int:
        cmp = self._read(addr, next(modes))
        i_ptr = self._read(addr+1, next(modes))

        if cmp == 0:
            return i_ptr

        # addr is i_ptr+1, and we have 2 parameters
        return addr+2

    # opcode 7 : less than
    def _less_than(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._read(addr, next(modes))
        r = self._read(addr+1, next(modes))

        out = 1 if l < r else 0

        self._write(addr+2, next(modes), out)
        return 4

    # opcode 8 : equals
    def _equals(self, addr: int, modes: Iterable[PMode]) -> int:
        l = self._read(addr, next(modes))
        r = self._read(addr+1, next(modes))

        out = 1 if l == r else 0

        self._write(addr+2, next(modes), out)
        return 4

    # opcode 9 : relative base offset
    def _rel_base_offset(self, addr: int, modes: Iterable[PMode]) -> int:
        offset = self._read(addr, next(modes))

        self.relative_base += offset

        return 2


def _interactive_commands(cpu, inputs, outputs):
    full_command = input("> ")
    if ' ' in full_command:
        command, args = full_command.split(' ', 1)
    else:
        command = full_command
        args = None

    match command:
        case "load":
            cpu.load_memory(args)
            return True
        case "run":
            if args:
                inputs.extend(map(int, args.split(',')))
            cpu.process()
            if outputs:
                print(outputs)
                outputs.clear()
            if cpu.halted():
                cpu.reset()
            return True
        case "inspect":
            print(f"memory: {cpu.memory} {cpu.sparse_memory}")
            print(f"i_ptr: {cpu.i_ptr}")
            return True
        case "help":
            print("load, run, inspect, exit, help")
            return True
        case "exit":
            return False
        case _:
            print(f"Unrecognized command '{command}', use 'help' for a list of commands")
            return True


def interactive():
    from collections import deque
    inputs = deque()
    outputs = []

    cpu = IntCode(input=inputs.popleft, output=outputs.append)

    while _interactive_commands(cpu, inputs, outputs):
        pass


if __name__ == "__main__":
    interactive()
