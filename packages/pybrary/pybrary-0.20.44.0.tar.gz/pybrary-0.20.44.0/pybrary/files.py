from re import compile, match
from os import scandir
from operator import attrgetter
from pathlib import Path
from functools import partial


def files(path):
    with scandir(path) as ls:
        for entry in sorted(ls, key=attrgetter('path')):
            if entry.is_dir(follow_symlinks=False):
                yield from files(entry.path)
            elif entry.is_file():
                yield entry.path


def find(path, name):
    match = compile(name).search
    for full in files(path):
        if match(full):
            yield Path(full)


def grep(rex, path):
    rmatch = partial(match, compile(rex))
    with open(path) as inp:
        for found in filter(None, map(rmatch, inp)):
            yield found.groups()

