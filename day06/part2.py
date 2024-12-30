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
        (x, y): 0
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
                lights[(x, y)] += 1
            elif 'off' in line:
                lights[(x, y)] = max(0, lights[(x, y)] - 1)
            elif 'toggle' in line:
                lights[(x, y)] += 2
            else:
                raise ValueError
    return sum(lights.values())


INPUT_S = '''\
toggle 0,0 through 999,999
'''
EXPECTED = 2000000


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
