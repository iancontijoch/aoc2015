from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def do(s: str) -> str:
    curr = s[0]
    cnt = 0
    ret = ''
    for i, c in enumerate(s):
        if curr == c:
            cnt += 1
        else:
            ret += f'{cnt}{s[i-1]}'
            curr = c
            cnt = 1
            if i == len(s) - 1:
                return f'{ret}{cnt}{c}'
    return ret


def compute(s: str) -> int:
    for _ in range(40):
        s = do(s.strip('\n'))
    return len(s)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1', 11),
        ('11', 21),
        ('21', 1211),
        ('1211', 111221),
        ('111221', 312211),
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
