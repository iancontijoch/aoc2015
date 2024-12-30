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
        cond1 = any(
            len(tuple(re.finditer(fr'{a}{b}', line))) > 1
            for a, b in zip(line, line[1:])
        )
        cond2 = any(a == c for a, _, c in zip(line, line[1:], line[2:]))
        if all((cond1, cond2)):
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('qjhvhtzxzqqjkmpb', 1),
        ('xxyxx', 1),
        ('uurcxstgmygtbstg', 0),
        ('ieodomkazucvgmuy', 0),
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
