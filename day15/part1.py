from __future__ import annotations

import argparse
import os.path

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    o = z3.Optimize()
    ingredient_qty_vars = dict()
    qty, stats = [], []

    for line in lines:
        name, scores_s = line.split(': ')
        name = name.lower()
        ingredient_qty_vars[f'{name}_qty'] = z3.Int(f'{name}_qty')
        qty.append(z3.Int(f'{name}_qty'))
        ingredient_stats = []
        for chunk in scores_s.split(', '):
            _, val = chunk.split()
            ingredient_stats.append(int(val))
        stats.append(ingredient_stats[:-1])

    o.add(z3.Sum([var for var in ingredient_qty_vars.values()]) == 100)
    o.add([var >= 0 for var in ingredient_qty_vars.values()])
    o.add([var <= 100 for var in ingredient_qty_vars.values()])

    sum_var = z3.Int('sum_var')

    def max(x: int, y: z3.Int) -> z3.ExprRef:
        return z3.If(x >= y, x, y)

    sum_var = z3.Product(
        [
            max(0, q * qty[0] + r * qty[1] + s * qty[2] + t * qty[3])
            for q, r, s, t in zip(*stats)
        ],
    )

    o.maximize(sum_var)

    if o.check() == z3.sat:
        return o.model().evaluate(sum_var)
    else:
        raise ValueError


INPUT_S = '''\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''
EXPECTED = 62842880


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
