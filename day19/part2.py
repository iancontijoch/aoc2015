from __future__ import annotations

import argparse
import os.path
from string import ascii_lowercase
from string import ascii_uppercase

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _split(s: str) -> list[str]:
    ret = []
    for i, c in enumerate(s):
        if c in ascii_lowercase:
            continue
        if c in ascii_uppercase and i == len(s) - 1:
            ret.append(c)
        elif c in ascii_uppercase and s[i+1] in ascii_lowercase:
            ret.append(c + s[i+1])
        else:
            ret.append(c)
    return ret


def compute(s: str) -> int:
    _, word = s.split('\n\n')
    word = word.strip('\n')
    return (
        len(_split(word)) -
        (word.count('Rn') + word.count('Ar')) -
        2 * word.count('Y') - 1
    )


INPUT_S = '''\
e => H
e => O
H => HO
H => OH
O => HH

HOH
'''
EXPECTED = 7


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
