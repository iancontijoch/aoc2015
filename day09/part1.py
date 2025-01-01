from __future__ import annotations

import argparse
import itertools
import os.path
import sys
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    graph = defaultdict(list)
    min_dist = sys.maxsize
    for line in lines:
        locations_s, dist_s = line.split(' = ')
        dist = int(dist_s)
        fr, to = locations_s.split(' to ')
        graph[fr].append((to, dist))
        graph[to].append((fr, dist))

    for path in itertools.permutations(graph, len(graph)):
        total = sum(
            dist
            for a, b in itertools.pairwise(path)
            for to, dist in graph[a]
            if to == b
        )
        if total < min_dist:
            min_dist = total
    return min_dist


INPUT_S = '''\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''
EXPECTED = 605


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
