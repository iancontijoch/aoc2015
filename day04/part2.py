from __future__ import annotations

import _md5
import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _get_key(s: str, n: int) -> str:
    return _md5.md5(str.encode(f'{s}{n}')).hexdigest()


def compute(s: str) -> int:
    s = s.strip('\n')
    n = 1
    while True:
        key = _get_key(s, n)
        if key[:6] == '0' * 6:
            return n
        n += 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('abcdef', 609043),
        ('pqrstuv', 1048970),
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
