from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ARROW_2_DIR = {
    '^': support.Direction4.UP,
    '>': support.Direction4.RIGHT,
    'v': support.Direction4.DOWN,
    '<': support.Direction4.LEFT,
}


def compute(s: str) -> int:
    start = (0, 0)
    seen = {start}
    for arrows_s in (s[::2], s[1::2]):
        pos = start
        for c in arrows_s:
            pos = ARROW_2_DIR.get(c, support.Direction4.UP).apply(*pos)
            seen.add(pos)

    return len(seen)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('^v', 3),
        ('^>v<', 3),
        ('^v^v^v^v^v', 11),
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
