from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _has_straight(s: str) -> bool:
    return any(
        ord(c) - ord(b) == 1
        and ord(b) - ord(a) == 1
        for a, b, c in zip(s, s[1:], s[2:])
    )


def _has_two_pairs(s: str) -> bool:
    return len(re.findall(r'(.)\1{1}', s)) > 1


def is_valid(s: str) -> bool:
    return (
        _has_straight(s)
        and _has_two_pairs(s)
        and all(c not in s for c in 'iol')
    )


def skip(s: str) -> str:
    matches = [m for m in re.finditer(r'[iol]', s)]
    if not matches:
        return s
    skip_idx = min(m.start(0) for m in matches)
    return s[:skip_idx + 1] + 'z' * len(s[skip_idx + 1:])


def increment(s: str) -> str:
    s = skip(s)
    start, end = s[:-1], s[-1]
    if end != 'z':
        return start + chr(ord(end) + 1)
    else:
        return increment(start) + 'a'


def find_password(s: str) -> str:
    s = increment(s)
    while not is_valid(s):
        s = increment(s)
    return s


def compute(s: str) -> str:
    lines = s.splitlines()
    for line in lines:
        password = find_password(line)
    return password


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('abcdefzz', 'abcdffaa'),
        ('ghijklmn', 'ghjaabcc'),
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
