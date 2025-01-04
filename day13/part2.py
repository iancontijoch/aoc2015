from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    prefs: dict[str, dict[str, int]] = defaultdict(dict)
    people: set[str] = set()
    lines = s.splitlines()
    for line in lines:
        line_lst = line[:-1].split()  # eliminate period
        p1, amt, p2 = line_lst[0], int(line_lst[3]), line_lst[-1]
        amt *= -1 if 'lose' in line else 1
        prefs[p1][p2] = amt
        people.update((p1, p2, 'Me'))

    for person in people:
        if person != 'Me':
            prefs[person]['Me'] = 0
            prefs['Me'][person] = 0

    orders = [list(x) for x in itertools.permutations(people)]
    orders = [[order[-1]] + order for order in orders]

    max_score = 0
    for order in orders:
        score = sum(
            prefs[a][b] + prefs[b][a]
            for a, b in itertools.pairwise(order)
        )
        max_score = max(score, max_score)

    return max_score


INPUT_S = '''\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''
EXPECTED = 330


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
