from __future__ import annotations

import argparse
import os.path
import sys

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)

    o = z3.Optimize()

    group = {n: z3.Int(f'group_{n}') for n in numbers}
    o.add([z3.And(group[n] >= 1, group[n] <= 4) for n in numbers])

    # group weights must be equal
    weights = {
        i: z3.Sum([
            z3.If(group[n] == i, n, 0)
            for n in numbers
        ])
        for i in range(1, 5)
    }
    o.add(weights[1] == weights[2])
    o.add(weights[1] == weights[3])
    o.add(weights[1] == weights[4])

    # minimize number of items in group 1
    num_group_1_items = z3.Sum(
        [z3.If(group[n] == 1, 1, 0) for n in numbers],
    )
    num_group_2_items = z3.Sum(
        [z3.If(group[n] == 2, 1, 0) for n in numbers],
    )
    num_group_3_items = z3.Sum(
        [z3.If(group[n] == 3, 1, 0) for n in numbers],
    )
    num_group_4_items = z3.Sum(
        [z3.If(group[n] == 4, 1, 0) for n in numbers],
    )

    o.add(
        z3.And(
            num_group_1_items > 0,
            num_group_1_items <= len(numbers) - 2,
            num_group_2_items > 0,
            num_group_2_items <= len(numbers) - 2,
            num_group_3_items > 0,
            num_group_3_items <= len(numbers) - 2,
            num_group_4_items > 0,
            num_group_4_items <= len(numbers) - 2,
        ),
    )

    o.add(num_group_1_items == 4)  # via trial and error

    quantum_entanglement = z3.Product(
        [z3.If(group[n] == 1, n, 1) for n in numbers],
    )

    min_qe = sys.maxsize
    # min_items = sys.maxsize
    while o.check() == z3.sat:
        m = o.model()

        # find out number of items in group 1 via
        # trial and error (to see what it converges to)
        # n_items = m.evaluate(num_group_1_items).as_long()
        # if n_items < min_items:
        #     min_items = n_items
        #     print(n_items)

        # find out minimum quantum entanglement via
        # trial and error (to see what it converges to)
        new_qe = m.evaluate(quantum_entanglement).as_long()
        if new_qe < min_qe:
            min_qe = new_qe
            print(new_qe)

    return 0


INPUT_S = '''\
1
2
3
4
5
7
8
9
10
11
'''
EXPECTED = 99


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
