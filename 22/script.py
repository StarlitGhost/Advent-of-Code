from copy import deepcopy
import sys
from GhostyUtils import aoc

spells = {
    'Magic Missile': {'mana': 53, 'other': {'dmg': 4}},
    'Drain': {'mana': 73, 'other': {'dmg': 2}, 'self': {'hp': 2}},
    'Shield': {'mana': 113, 'self': {'duration': 6, 'arm': 7}},
    'Poison': {'mana': 173, 'other': {'duration': 6, 'dmg': 3}},
    'Recharge': {'mana': 229, 'self': {'duration': 5, 'mana': 101}},
}


def effects_tick(entity: dict) -> None:
    ended = []

    for name, effect in entity['effects'].items():
        if 'dmg' in effect:
            entity['hp'] -= effect['dmg']
        if 'arm' in effect:
            entity['arm'] = effect['arm']
        if 'mana' in effect:
            entity['mana'] += effect['mana']

        effect['duration'] -= 1
        if effect['duration'] <= 0:
            if 'arm' in effect:
                entity['arm'] = 0
            ended.append(name)

    for name in ended:
        del entity['effects'][name]


def cast_spell(spell_name: str, player: dict, boss: dict) -> int:
    spell = spells[spell_name]

    player['mana'] -= spell['mana']

    if 'self' in spell:
        self = spell['self']
        if 'duration' in self:
            player['effects'][spell_name] = self.copy()
        elif 'hp' in self:
            player['hp'] += self['hp']

    if 'other' in spell:
        other = spell['other']
        if 'duration' in other:
            boss['effects'][spell_name] = other.copy()
        elif 'dmg' in other:
            boss['hp'] -= other['dmg']

    return spell['mana']


def take_turns(player: dict, boss: dict, turn: int = 0,
               mana_spent: int = 0, least_mana: int = sys.maxsize,
               p2: bool = False) -> int:
    # p2, drain the player's hp by 1 before all other effects
    if p2 and turn % 2 == 0:
        player['hp'] -= 1
        if player['hp'] <= 0:
            return least_mana

    # apply effects
    effects_tick(player)
    effects_tick(boss)

    # we beat the boss with effect damage!
    if boss['hp'] <= 0:
        if mana_spent < least_mana:
            return mana_spent
        else:
            return least_mana

    if turn % 2 == 0:  # player turn

        # what spells can we cast?
        spells_available = []
        for name, spell in spells.items():
            # not enough mana
            if player['mana'] < spell['mana']:
                continue
            # effect still ticking
            if name in player['effects'] or name in boss['effects']:
                continue
            spells_available.append(name)

        # prioritise spells by mana cost, lowest first
        spells_available.sort(key=lambda name: spells[name]['mana'])

        # we lose if we can't cast spells
        if not spells_available:
            return least_mana

        # let's cast!
        for spell in spells_available:
            p = deepcopy(player)
            b = deepcopy(boss)
            spell_cost = cast_spell(spell, p, b)

            if mana_spent + spell_cost >= least_mana:
                return least_mana

            # we beat the boss with our spell!
            if boss['hp'] <= 0:
                if mana_spent + spell_cost < least_mana:
                    return mana_spent + spell_cost
                else:
                    return least_mana

            result = take_turns(p, b, turn+1,
                                mana_spent + spell_cost, least_mana,
                                p2)
            if result < least_mana:
                least_mana = result
                continue
        return least_mana

    else:  # boss turn
        player['hp'] -= max(boss['dmg'] - player['arm'], 0)

        # we died!
        if player['hp'] <= 0:
            return least_mana

        return take_turns(player, boss, turn+1, mana_spent, least_mana, p2)


if __name__ == '__main__':
    inputs = aoc.read_lines()

    player = {
        'hp': 50,
        'mana': 500,
        'arm': 0,
        'effects': {},
    }
    boss = {
        'hp': int(inputs[0].split(': ')[1]),
        'dmg': int(inputs[1].split(': ')[1]),
        'effects': {},
    }

    least_mana = take_turns(deepcopy(player), deepcopy(boss))
    print(least_mana)
    least_mana = take_turns(deepcopy(player), deepcopy(boss), p2=True)
    print(least_mana)
