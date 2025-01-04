from __future__ import annotations

import argparse
import json
import os.path
from collections.abc import Generator
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _flatten(nested_lst: Any) -> Generator[Any]:
    for item in nested_lst:
        if isinstance(item, list):
            yield from _flatten(item)
        else:
            yield item


def sum_ignore_red(obj: Any, red_objs: list[Any], parent: Any = None) -> int:
    if obj in red_objs or parent is not None and parent in red_objs:
        return 0
    elif isinstance(obj, str):
        return 0
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum(sum_ignore_red(x, red_objs, obj) for x in obj)
    elif isinstance(obj, dict):
        return sum(sum_ignore_red(v, red_objs, obj) for v in obj.values())
    else:
        raise ValueError(obj, parent)


def _red_objs(obj: Any, parent: Any = None) -> Any:
    if isinstance(obj, int) or isinstance(obj, str):
        if obj == 'red' and isinstance(parent, dict):
            return parent
        else:
            return
    else:
        if isinstance(obj, list):
            return [_red_objs(x, obj) for x in obj]
        elif isinstance(obj, dict):
            return [_red_objs(v, obj) for v in obj.values()]
        else:
            raise ValueError(obj)


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        obj = json.loads(line)
        red_objs = list(_flatten(_red_objs(obj)))
        total += sum_ignore_red(obj, red_objs)
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
