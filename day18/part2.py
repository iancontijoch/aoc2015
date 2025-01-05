from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords(s)
    bx, by = support.bounds(coords)
    # support.print_coords(coords)
    corners = (
        (bx.min, by.min),
        (bx.min, by.max),
        (bx.max, by.min),
        (bx.max, by.max),
    )

    coords.update({pos: '#' for pos in corners})
    for _ in range(100):
        on = {pos for pos, c in coords.items() if c == '#'}
        new_on = set()
        new_off = set()

        for pos in coords:
            if pos in corners:
                continue
            num_on = len(
                {adj for adj in support.adjacent_8(*pos) if adj in on},
            )
            if pos in on and num_on not in (2, 3):
                new_off.add(pos)
            if pos not in on and num_on == 3:
                new_on.add(pos)

        coords.update({pos: '#' for pos in new_on})
        coords.update({pos: '.' for pos in new_off})
        # print()
        # support.print_coords(coords)
    return len({pos for pos, c in coords.items() if c == '#'})


INPUT_S = '''\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''
EXPECTED = 17


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
