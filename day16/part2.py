from __future__ import annotations

import argparse
import os.path
from collections.abc import Callable

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    counts = {
        'children': lambda x: x == 3,
        'cats': lambda x: x > 7,
        'samoyeds': lambda x: x == 2,
        'pomeranians': lambda x: x < 3,
        'akitas': lambda x: x == 0,
        'vizslas': lambda x: x == 0,
        'goldfish': lambda x: x < 5,
        'trees': lambda x: x > 3,
        'cars': lambda x: x == 2,
        'perfumes': lambda x: x == 1,
    }

    def check(s: str, counts: dict[str, Callable[[int], bool]]) -> bool:
        for chunk in s.split(', '):
            k, v = chunk.split(': ')
            if not counts[k](int(v)):
                return False
        return True

    lines = s.splitlines()
    for line in lines:
        id_num = int(line.split()[1][:-1])
        items_s = ' '.join(line.split()[2:])
        if check(items_s, counts):
            return id_num
    return 0


INPUT_S = '''\
Sue 1: children: 1, cars: 8, vizslas: 7
Sue 2: akitas: 10, perfumes: 10, children: 5
Sue 3: cars: 5, pomeranians: 4, vizslas: 1
Sue 213: children: 3, goldfish: 5, vizslas: 0
'''
EXPECTED = 213


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
