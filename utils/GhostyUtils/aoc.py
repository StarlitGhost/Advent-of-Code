import argparse
from typing import Iterable

_parser = argparse.ArgumentParser()
_parser.add_argument('filename', nargs='?', default='input', help="the input filename")
_parser.add_argument('-v', '--verbose', action='store_true', help="verbose output")
_parser.add_argument('-p', '--progress', action='store_true', help="progress output")
_args = None


def __getattr__(name):
    properties = {
        'argparser': _argparser,
        'args': _get_args,
    }
    if name in properties:
        return properties[name]()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def _argparser():
    global _parser
    return _parser


def _get_args():
    global _args
    if _args is None:
        _args = _parser.parse_args()
    return _args


def _get_filename(file: str) -> str:
    global _args
    global _parser
    _args = _parser.parse_args()
    return _args.filename


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
