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
        l, w, h = map(int, line.split('x'))
        total += 2 * min(l + w, l + h, w + h) + (l * w * h)

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('2x3x4', 34),
        ('1x1x10', 14),
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
