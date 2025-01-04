from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        total += sum(map(int, re.findall(r'-*\d+', line)))
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('[1,2,3]', 6),
        ('{"a":2,"b":4}', 6),
        ('[[[3]]]', 3),
        ('{"a":{"b":4},"c":-1}', 3),
        ('{"a":[-1,1]}', 0),
        ('[-1,{"a":1}]', 0),
        ('[]', 0),
        ('{}', 0),
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
