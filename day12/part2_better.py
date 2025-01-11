from __future__ import annotations

import argparse
import json
import os.path
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def traverse(v: Any) -> int:
    if isinstance(v, int):
        return v
    elif isinstance(v, str):
        return 0
    elif isinstance(v, list):
        return sum(traverse(x) for x in v)
    elif isinstance(v, dict):
        if 'red' in v.values():
            return 0
        return sum(traverse(v2) for v2 in v.values())
    else:
        raise NotImplementedError


def compute(s: str) -> int:
    total, d = 0, json.loads(s)
    for _, v in d.items():
        if 'red' not in d.values():
            total += traverse(v)
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('[1,2,3]', 6),
        ('[1,{"c":"red","b":2},3]', 4),
        ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
        ('[1,"red",5]', 6),
        ('[1, [2, [{"a": "red", "b": [1, 2, {"c": 2}]}]], 3]', 6),
        ('[1, [2, {"a": "red", "b": 2}, {"a": "red", "b": 2}]]', 3),
        ('[1,{"c":2,"b":-1,"a": [1, 2, "red"]},-1]', 4),
        ('[-1, {"d":"red","e":[1,2,3,4],"f":5}]', -1),
        ('[{"a": "red", "b": 1}]', 0),

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
