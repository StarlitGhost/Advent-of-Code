import sys
from typing import Iterable


def read(file: str = None) -> str:
    if file is None:
        if len(sys.argv) > 1:
            file = sys.argv[1]
        else:
            file = 'input'
    return open(file).read().strip()


def read_lines(file: str = None) -> Iterable[str]:
    return read(file).splitlines()


def read_sections(file: str = None, split: str = '\n\n') -> Iterable[str]:
    return read(file).split(split)
