from __future__ import annotations

import argparse
import copy
import os.path
import sys
from collections import deque
from dataclasses import dataclass
from enum import auto
from enum import Enum

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Stat(Enum):
    HP = auto()
    ARMOR = auto()
    DAMAGE = auto()
    MANA = auto()


class SpellType(Enum):
    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()


@dataclass
class Player():
    name: str
    hp: int
    mana: int = 0
    damage: int = 0
    armor: int = 0
    mana_spent: int = 0

    def status(self) -> str:
        if self.name == 'Player':
            return (
                f'-{self.name.capitalize()} has '
                f'{self.hp} hit points, {self.armor} armor, '
                f'{self.mana} mana'
            )
        else:
            return (f'-{self.name.capitalize()} has '
                    f'{self.hp} hit points')

    def cast(self, spell: Spell, boss: Player) -> Effect | None:
        self.mana -= spell.cost
        self.mana_spent += spell.cost
        if spell.effect is None:
            spell.apply(self, boss)
        return spell.effect


@dataclass
class Effect():
    stat: Stat
    amt: int
    spell_timer: int
    spell_name: str
    timer: int
    is_active: bool = False
    is_immediate: bool = False

    def __gt__(self, effect: Effect) -> bool:
        return self.stat.name > effect.stat.name

    def __lt__(self, effect: Effect) -> bool:
        return self.stat.name < effect.stat.name

    def apply(self, player: Player, boss: Player) -> None:
        if self.timer > 0:
            self.is_active = True

            if self.stat is Stat.HP:
                player.hp += self.amt
            if self.stat is Stat.DAMAGE:
                boss.hp -= self.amt
            if self.stat is Stat.ARMOR and self.timer == self.spell_timer:
                player.armor += self.amt
            if self.stat is Stat.MANA:
                player.mana += self.amt
            self.timer -= 1
            self.timer = max(self.timer, 0)
        if self.timer == 0:
            self.is_active = False
            if self.stat is Stat.ARMOR:
                player.armor -= 7


@dataclass
class Spell():
    name: str
    cost: int
    damage: int = 0
    hp: int = 0
    effect: Effect | None = None
    is_active: bool = False

    @staticmethod
    def get(spell_type: SpellType) -> Spell:
        return {
            SpellType.MAGIC_MISSILE: Spell(
                name='magic_missile',
                damage=4,
                cost=53,
            ),
            SpellType.DRAIN: Spell(name='drain', damage=2, hp=2, cost=73),
            SpellType.SHIELD: Spell(
                name='shield',
                effect=Effect(
                    stat=Stat.ARMOR,
                    amt=7,
                    timer=7,
                    spell_timer=7,
                    spell_name='shield',
                    is_immediate=True,
                ),
                cost=113,
            ),
            SpellType.POISON: Spell(
                name='poison',
                effect=Effect(
                    stat=Stat.DAMAGE,
                    amt=3,
                    timer=6,
                    spell_timer=6,
                    spell_name='poison',
                ),
                cost=173,
            ),
            SpellType.RECHARGE: Spell(
                name='recharge',
                effect=Effect(
                    stat=Stat.MANA,
                    amt=101, timer=5,
                    spell_timer=5,
                    spell_name='recharge',
                ),
                cost=229,
            ),
        }.get(
            spell_type, Spell(
                name='magic_missile',
                damage=4,
                cost=53,
            ),
        )

    def apply(self, player: Player, boss: Player) -> None:
        player.hp += self.hp
        boss.hp -= self.damage


def print_state(
    p1: Player, p2: Player,
    turn: str, active_effects: list[Effect],
) -> None:
    print(f'--{turn.capitalize()} turn--')
    print(p1.status())
    print(p2.status())
    print('active effects: ', active_effects)


def game_loop(
    p1: Player, p2: Player, t: int,
    active_effects: list[Effect] | None = None,
) -> int:
    min_mana = sys.maxsize
    todo: deque[
        tuple[Player, Player, list[Effect], int, list[str]]
    ] = deque([(p1, p2, [], 0, [])])
    game_over = False

    winning_states = set()
    losing_states = set()

    while todo:
        # print(todo)
        p1, p2, active_effects, t, path = todo.pop()
        turn = 'player' if t % 2 == 0 else 'boss'
        state = f'{p1}{p2}{sorted(active_effects)}{turn}'

        if state in winning_states or state in losing_states:
            continue

        if p1.mana_spent >= min_mana:
            continue

        # execute active effects at start of turn and check if it ends the game
        for effect in active_effects:
            effect.apply(p1, p2)

            # check health
            if p1.hp <= 0:
                losing_states.add(state)
                game_over = True
                break
            if p2.hp <= 0:
                winning_states.add(state)
                min_mana = min(min_mana, p1.mana_spent)
                game_over = True
                break

        active_effects = [
            effect for effect in active_effects if effect.timer > 0
        ]

        if game_over:
            game_over = False
            continue

        # take actions
        if turn == 'boss':
            p1.hp -= max(1, p2.damage - p1.armor)
            todo.append((
                p1, p2, active_effects, t + 1, path +
                [f'{p1.hp} {p2.hp} {p1.mana} {p1.armor}'],
            ))

        else:
            # player chooses a spell and casts it
            spells = [Spell.get(s) for s in SpellType]

            if p1.mana < 53:
                losing_states.add(state)
                game_over = True
                continue

            possible_next_spells = [
                s for s in spells
                if p1.mana >= s.cost and (
                    s.effect is None or
                    s.effect.spell_name not in (
                        e.spell_name for e in active_effects
                    )
                )
            ]

            for spell in possible_next_spells:
                p1_alt = copy.copy(p1)
                p2_alt = copy.copy(p2)
                active_effects_alt = [copy.copy(e) for e in active_effects]

                # add new effects (if any) from casting spell)
                # will do immediate actions except shield
                new_effect = p1_alt.cast(spell, p2_alt)

                state = f'{p1_alt}{p2_alt}{sorted(active_effects_alt)}{turn}'

                if state in winning_states or state in losing_states:
                    continue

                # check if this ends the game
                if p1_alt.hp <= 0:
                    losing_states.add(state)
                    game_over = True
                    break
                if p2_alt.hp <= 0:
                    winning_states.add(state)
                    min_mana = min(min_mana, p1_alt.mana_spent)
                    game_over = True
                    break

                if new_effect is not None:
                    active_effects_alt.append(new_effect)
                for effect in active_effects_alt:
                    if (
                        effect.is_immediate and
                        effect.timer == effect.spell_timer
                    ):  # only shield
                        effect.apply(p1_alt, p2_alt)

                # forward the state to the next turn
                active_effects_alt = [
                    effect for effect in active_effects_alt if effect.timer > 0
                ]
                todo.append((
                    p1_alt, p2_alt, active_effects_alt, t + 1, path +
                    [f'{spell.name} {p1_alt.hp} {p2_alt.hp}'
                     f'{p1_alt.mana} {p1_alt.armor}'],
                ))

            if game_over:
                game_over = False
                continue
    return min_mana


def compute(s: str) -> int:
    p1, p2 = Player(name='Player', hp=50, mana=500), Player(
        name='Boss', hp=58, damage=9,
    )

    min_mana = game_loop(p1=p1, p2=p2, t=0)
    return min_mana


INPUT_S = '''\

'''
EXPECTED = 1


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
