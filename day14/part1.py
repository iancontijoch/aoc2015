from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Deer():
    name: str
    speed: int
    fly_time: int
    rest_time: int
    time_left: int = 2503
    distance: int = 0
    next_state: str = 'fly'

    def rest(self) -> None:
        self.time_left -= self.rest_time

    def move(self) -> None:
        if self.next_state == 'fly':
            self.next_state = 'rest'
            avail_time = min(self.time_left, self.fly_time)
            self.distance += self.speed * avail_time
            self.time_left -= avail_time
            self.time_left = max(0, self.time_left)
        else:
            self.rest()
            self.next_state = 'fly'


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

    for deer in deersies:
        while deer.time_left > 0:
            deer.move()

    return max(deer.distance for deer in deersies)


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
