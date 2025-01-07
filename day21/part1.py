from __future__ import annotations

import argparse
import itertools
import math
import os.path
import sys
from dataclasses import dataclass
from enum import auto
from enum import Enum

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    RING = auto()


@dataclass
class Item():
    name: str
    cost: int
    damage: int
    armor: int
    type: ItemType


@dataclass
class Player():
    name: str
    hp: int = 100
    dmg: int = 0
    armor: int = 0
    cost: int = 0
    equipped_weapon: Item | None = None
    equipped_armor: Item | None = None
    equipped_rings: list[Item] | None = None

    def equip(self, item: Item) -> None:
        if self.equipped_rings is None:
            self.equipped_rings = []

        if item.type is ItemType.WEAPON and self.equipped_weapon is not None:
            return
        if item.type is ItemType.ARMOR and self.equipped_armor is not None:
            return
        if item.type is ItemType.RING and len(self.equipped_rings) == 2:
            return

        if item.type is ItemType.WEAPON:
            self.equipped_weapon = item
        elif item.type is ItemType.ARMOR:
            self.equipped_armor = item
        else:
            self.equipped_rings.append(item)

        self.dmg += item.damage
        self.armor += item.armor
        self.cost += item.cost

    def unequip(self, item_type: ItemType) -> None:
        item_mapping = {
            ItemType.WEAPON: 'equipped_weapon',
            ItemType.ARMOR: 'equipped_armor',
            ItemType.RING: 'equipped_rings',
        }

        equipped_item = getattr(self, item_mapping[item_type])

        if equipped_item:
            if item_type is ItemType.RING:
                self.dmg -= sum(
                    ring.damage for ring in equipped_item
                    if ring is not None
                )
                self.armor -= sum(
                    ring.armor for ring in equipped_item
                    if ring is not None
                )
                self.cost -= sum(
                    ring.cost for ring in equipped_item
                    if ring is not None
                )
            else:
                self.dmg -= equipped_item.damage
                self.armor -= equipped_item.armor
                self.cost -= equipped_item.cost

        # set equipped item to None
        setattr(self, item_mapping[item_type], None)


def wins_fight(p1: Player, p2: Player) -> bool:
    dmg_p1 = max(1, p1.dmg - p2.armor)
    dmg_p2 = max(1, p2.dmg - p1.armor)

    p1_n_turns = math.ceil(p1.hp / dmg_p2)
    p2_n_turns = math.ceil(p2.hp / dmg_p1)
    return p1_n_turns >= p2_n_turns


def equip_p1(
    p1: Player,
    weapon: Item,
    armor: Item | None,
    rings: tuple[Item | None, Item | None],
) -> Player:
    p1.equip(weapon)
    if armor is not None:
        p1.equip(armor)
    if rings is not None:
        for ring in rings:
            if ring is not None:
                p1.equip(ring)
    return p1


def _get_items() -> tuple[list[Item], list[Item | None], list[Item | None]]:
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

    weapons = []
    armors: list[Item | None] = [None]
    rings: list[Item | None] = [None, None]

    for i, section in enumerate(s.split('\n\n')):
        for line in section.splitlines()[1:]:
            name, cost_s, damage_s, armor_s = line.split()
            cost, damage, armor = map(int, (cost_s, damage_s, armor_s))
            if i == 0:
                weapons.append(
                    Item(name, cost, damage, armor, ItemType.WEAPON),
                )
            elif i == 1:
                armors.append(
                    Item(name, cost, damage, armor, ItemType.ARMOR),
                )
            else:
                rings.append(
                    Item(name, cost, damage, armor, ItemType.RING),
                )

    armors.extend([None])
    rings.extend([None, None])

    return weapons, armors, rings


def compute(s: str) -> int:
    p1 = Player(name='You', hp=100)
    p2 = Player(name='Boss', hp=100, dmg=8, armor=2)

    min_cost = sys.maxsize
    weapons, armors, rings = _get_items()
    # try everything
    for weapon in weapons:
        for armor in armors:
            for ring_combo in itertools.combinations(rings, 2):
                p1 = equip_p1(p1, weapon, armor, ring_combo)
                if wins_fight(p1, p2):
                    min_cost = min(min_cost, p1.cost)
                p1.unequip(ItemType.RING)
            p1.unequip(ItemType.ARMOR)
        p1.unequip(ItemType.WEAPON)

    return min_cost


INPUT_S = '''\
Hit Points: 100
Damage: 8
Armor: 2
'''
EXPECTED = 10


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
