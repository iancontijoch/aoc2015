from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    lights = {
        (x, y): False
        for y in range(0, 1000)
        for x in range(0, 1000)
    }

    for line in lines:
        rng1, rng2 = (
            tuple(map(int, group))
            for group in (
                m.groups()
                for m in re.finditer(r'(\d+),(\d+)', line)
            )
        )
        rng = (
            (x, y)
            for y in range(rng1[1], rng2[1] + 1)
            for x in range(rng1[0], rng2[0] + 1)
        )
        for x, y in rng:
            if 'on' in line:
                lights[(x, y)] = True
            elif 'off' in line:
                lights[(x, y)] = False
            elif 'toggle' in line:
                lights[(x, y)] = not lights[(x, y)]
            else:
                raise ValueError
    return sum(lights.values())


INPUT_S = '''\
turn on 0,0 through 999,999
'''
EXPECTED = 1000 * 1000


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
