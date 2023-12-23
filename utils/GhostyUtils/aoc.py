import sys
from typing import Iterable


def _get_filename(file: str) -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return 'input'


def _generator(file: str = None):
    if file is None:
        file = _get_filename(file)
    return open(file)


def read(file: str = None) -> str:
    return _generator(file).read().strip()


def read_lines(file: str = None) -> list[str]:
    return read(file).splitlines()


def read_sections(file: str = None, split: str = '\n\n') -> list[str]:
    return read(file).split(split)


def by_lines(file: str = None) -> Iterable[str]:
    for line in _generator(file):
        yield line
