from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
SECONDS = 2503


@dataclass
class Deer():
    name: str
    speed: int
    fly_time: int
    rest_time: int


def dist_at_time(deer: Deer, t: int) -> int:
    distances = (deer.speed,) * deer.fly_time + (0,) * deer.rest_time
    dist_cycle = itertools.cycle(distances)
    sum = 0
    for _ in range(t):
        sum += next(dist_cycle)
    return sum


def compute(s: str) -> int:
    lines = s.splitlines()
    deersies = []
    for line_s in lines:
        line = line_s[:-1].split()  # remove period
        deersies.append(
            Deer(
                name=line[0], speed=int(line[3]), fly_time=int(
                    line[6],
                ), rest_time=int(line[-2]),
            ),
        )

    leaderboard: dict[str, int] = defaultdict(int)

    for t in range(1, SECONDS + 1):
        max_dist = max(dist_at_time(deer, t) for deer in deersies)
        winners = tuple(
            deer.name for deer in deersies if dist_at_time(deer, t) == max_dist
        )
        for winner in winners:
            leaderboard[winner] += 1

    return max(leaderboard.values())


INPUT_S = '''\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''
EXPECTED = 1120


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
