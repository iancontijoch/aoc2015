from __future__ import annotations

import argparse
import os.path
import sys

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _get_items() -> tuple[
    dict[str, z3.Int],
    dict[str, z3.Int],
    dict[str, z3.Int],
    list[dict[str, int]],
]:
    s = '''\
    Weapons:    Cost  Damage  Armor
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0

    Armor:      Cost  Damage  Armor
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5

    Rings:      Cost  Damage  Armor
    Damage+1    25     1       0
    Damage+2    50     2       0
    Damage+3   100     3       0
    Defense+1   20     0       1
    Defense+2   40     0       2
    Defense+3   80     0       3'''

    weapons = dict()
    armors = dict()
    rings = dict()

    specs: list[dict[str, int]] = []

    cost_specs = dict()
    damage_specs = dict()
    armor_specs = dict()

    for i, section in enumerate(s.split('\n\n')):
        for line in section.splitlines()[1:]:
            name, cost_s, damage_s, armor_s = line.split()
            name = name.lower()
            cost, damage, armor = map(int, (cost_s, damage_s, armor_s))
            if i == 0:
                weapons[name] = z3.Int(name)
            elif i == 1:
                armors[name] = z3.Int(name)
            else:
                rings[name] = z3.Int(name)

            cost_specs[name] = cost
            damage_specs[name] = damage
            armor_specs[name] = armor
    specs.extend(
        spec_dct for spec_dct in (
            cost_specs, damage_specs, armor_specs,
        )
    )
    return weapons, armors, rings, specs


def compute(s: str) -> int:
    min_cost = sys.maxsize
    weapons, armors, rings, specs = _get_items()
    cost_specs, damage_specs, armor_specs = specs

    o = z3.Optimize()
    o.add([0 <= e for e in weapons.values()])
    o.add([e <= 1 for e in weapons.values()])
    o.add(z3.Sum([e for e in weapons.values()]) == 1)

    o.add([0 <= e for e in armors.values()])
    o.add([e <= 1 for e in armors.values()])
    o.add(z3.Sum([e for e in armors.values()]) == 1)

    o.add([0 <= e for e in rings.values()])
    o.add([e <= 1 for e in rings.values()])
    o.add(z3.Sum([e for e in rings.values()]) >= 0)
    o.add(z3.Sum([e for e in rings.values()]) <= 2)

    total_cost = (
        z3.Sum([
            e_var * cost_specs[e_key]
            for e_key, e_var in weapons.items()
        ]) +
        z3.Sum([
            e_var * cost_specs[e_key]
            for e_key, e_var in armors.items()
        ]) +
        z3.Sum([
            e_var * cost_specs[e_key]
            for e_key, e_var in rings.items()
        ])
    )

    p1_damage = (
        z3.Sum([
            e_var * damage_specs[e_key]
            for e_key, e_var in weapons.items()
        ]) +
        z3.Sum([
            e_var * damage_specs[e_key]
            for e_key, e_var in armors.items()
        ]) +
        z3.Sum([
            e_var * damage_specs[e_key]
            for e_key, e_var in rings.items()
        ])
    )

    p1_armor = (
        z3.Sum([
            e_var * armor_specs[e_key]
            for e_key, e_var in weapons.items()
        ]) +
        z3.Sum([
            e_var * armor_specs[e_key]
            for e_key, e_var in armors.items()
        ]) +
        z3.Sum([
            e_var * armor_specs[e_key]
            for e_key, e_var in rings.items()
        ])
    )

    def _max(x: int, y: z3.Int) -> z3.ExprRef:
        return z3.If(y < 1, 1, y)

    def wins_fight(
        p1_hp: int, p2_hp: int,
        p1_dmg: z3.Int, p2_dmg: int,
        p1_armor: z3.Int, p2_armor: int,
    ) -> z3.ExprRef:
        p1_dmg = _max(1, p1_dmg - p2_armor)
        p2_dmg = _max(1, p2_dmg - p1_armor)

        p1_n_turns = p1_hp / p2_dmg
        p2_n_turns = p2_hp / p1_dmg
        return p1_n_turns >= p2_n_turns

    o.add(
        wins_fight(
            p1_hp=100, p2_hp=100, p1_dmg=p1_damage,
            p2_dmg=8, p1_armor=p1_armor, p2_armor=2,
        ),
    )

    o.minimize(total_cost)

    if o.check() == z3.sat:
        return o.model().evaluate(total_cost)
    return min_cost


INPUT_S = '''\
Hit Points: 100
Damage: 8
Armor: 2
'''
EXPECTED = 91


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
