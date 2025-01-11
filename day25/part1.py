from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def next_pos(x: int, y: int) -> tuple[int, int]:
    if y == 1:
        return 1, x + 1
    else:
        return x + 1, y - 1


def compute(s: str) -> int:
    start = (1, 1)
    end = (3029, 2947)
    coords = {start: 20151125}
    pos = start
    while pos != end:
        nxt = next_pos(*pos)
        coords[nxt] = (coords[pos] * 252533) % 33554393
        pos = nxt

    return coords[end]


INPUT_S = '''\
1
'''
EXPECTED = 1


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
