from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        cond1 = sum(c in 'aeiou' for c in line) >= 3
        cond2 = any(a == b for a, b in zip(line, line[1:]))
        cond3 = all(st not in line for st in ('ab', 'cd', 'pq', 'xy'))
        if all((cond1, cond2, cond3)):
            total += 1

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ugknbfddgicrmopn', 1),
        ('aaa', 1),
        ('jchzalrnumimnmhp', 0),
        ('haegwjzuvuyypxyu', 0),
        ('dvszwmarrgswjxmb', 0),
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
