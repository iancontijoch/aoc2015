from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
LITERS = 150


def compute(s: str) -> int:
    total = 0
    weights = [int(line) for line in s.splitlines()]
    for combo in itertools.product((0, 1), repeat=len(weights)):
        if sum(w * c for w, c in zip(weights, combo)) == LITERS:
            total += 1

    return total


INPUT_S = '''\
20
15
10
5
5
'''
EXPECTED = 4


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
