from __future__ import annotations

import argparse
import functools
import os.path

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@functools.cache
def get_factors(n: int) -> set[int]:
    factors = set()
    i = 1
    while i ** 2 <= n:
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
        i += 1
    return factors


def score(n: int) -> int:
    return 10 * sum(get_factors(n))


def compute(s: str) -> int:
    n = int(s)
    i = 0
    while score(i) < n:
        i += 1
    return i


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1', 10),
        ('2', 30),
        ('3', 40),
        ('4', 70),
        ('5', 60),
        ('6', 120),
        ('7', 80),
        ('8', 150),
        ('9', 130),
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
