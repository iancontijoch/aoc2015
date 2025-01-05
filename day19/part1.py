from __future__ import annotations

import argparse
import os.path
import re
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    replacements = defaultdict(list)
    new_words: set[str] = set()

    replacements_s, word = s.split('\n\n')
    word = word.strip('\n')

    for line in replacements_s.splitlines():
        fr, to = line.split(' => ')
        replacements[fr].append(to)

    for fr, to_lst in replacements.items():
        for m in re.finditer(fr, word):
            before, after = word[:m.start()], word[m.end():]
            new_words.update(before + to + after for to in to_lst)
    return len(new_words)


INPUT_S = '''\
H => HO
H => OH
O => HH

HOHOHO
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
