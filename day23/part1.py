from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _get_offset(s: str) -> int:
    if s[0] == '+':
        return int(s[1:])
    else:
        return -int(s[1:])


def compute(s: str) -> int:
    lines = s.splitlines()
    regs = {'a': 0, 'b': 0}

    i = 0
    while i < len(lines):
        nxt = lines[i]
        match nxt.replace(',', '').split():
            case ['hlf', r]:
                regs[r] //= 2
                i += 1
            case ['tpl', r]:
                regs[r] *= 3
                i += 1
            case ['inc', r]:
                regs[r] += 1
                i += 1
            case ['jmp', offset]:
                i += _get_offset(offset)
            case ['jie', r, offset]:
                if regs[r] % 2 == 0:
                    i += _get_offset(offset)
                else:
                    i += 1
            case ['jio', r, offset]:
                if regs[r] == 1:
                    i += _get_offset(offset)
                else:
                    i += 1

    return regs['b']


INPUT_S = '''\
inc a
jio a, +2
tpl a
inc a
'''
EXPECTED = 2


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
