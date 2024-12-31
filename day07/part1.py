from __future__ import annotations

import argparse
import operator
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {
    'AND': operator.and_,
    'OR': operator.or_,
    'LSHIFT': operator.lshift,
    'RSHIFT': operator.rshift,
    'NOT': operator.inv,
}


def compute(s: str, w: str) -> int:
    wires: dict[str, int] = dict()
    lines = s.splitlines()
    todo = deque(lines)
    while todo:
        line = todo.popleft()
        input_s, output = line.split(' -> ')
        match input_s.split():
            case [w1_s] if w1_s.isalpha():
                if w1_s in wires:
                    wires[output] = wires[w1_s]
                else:
                    todo.append(line)
                    continue
            case [w1_s] if w1_s.isnumeric():
                wires[output] = int(w1_s)
            case ['NOT', w1_s]:
                if w1_s in wires:
                    wires[output] = (
                        2 ** 16 - 1 -
                        (
                            int(w1_s) if w1_s.isnumeric()
                            else wires[w1_s]
                        )
                    )
                else:
                    todo.append(line)
                    continue
            case [w1_s, op_s, w2_s]:
                if any(
                    w_s.isalpha()
                    and w_s not in wires
                    for w_s in (w1_s, w2_s)
                ):
                    todo.append(line)
                    continue
                w1 = int(w1_s) if w1_s.isnumeric() else wires[w1_s]
                w2 = int(w2_s) if w2_s.isnumeric() else wires[w2_s]
                wires[output] = OPS.get(op_s)(w1, w2)  # type: ignore
    return wires.get(w, -1)


INPUT_S = '''\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
'''
EXPECTED = 65079


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 'i') == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 'a'))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
