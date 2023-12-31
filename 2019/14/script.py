from GhostyUtils import aoc
import math
from collections import defaultdict, deque


def ore_for_n_fuel(fuel: int, reactions: dict) -> int:
    required = deque()
    required.append(('FUEL', fuel))
    leftovers = defaultdict(int)
    ore = 0

    # while we still have chemicals to make...
    while required:
        # take a chemical from the queue
        product, amount = required.popleft()

        # use materials from our leftover pile, if we have enough to cover the whole cost
        if amount <= leftovers[product]:
            leftovers[product] -= amount
            continue

        # use up any leftovers we might have
        to_create = amount - leftovers[product]
        del leftovers[product]

        # calculate how many reactions we need to do
        creates = reactions[product]['creates']
        num_reactions = math.ceil(to_create / creates)

        # add leftovers to our pile
        leftover = (creates * num_reactions) - to_create
        leftovers[product] += leftover

        # add all the reactants to make this product to the queue
        for reactant, amount in reactions[product]['reactants'].items():
            # if our reactant is ore, add to the ore count instead
            if reactant == 'ORE':
                ore += amount * num_reactions
            else:
                required.append((reactant, amount * num_reactions))

    return ore


def main():
    reactions_txt = aoc.read_lines()

    reactions = {}
    for reaction in reactions_txt:
        input, output = reaction.split(' => ')
        inputs = input.split(', ')
        amount, name = output.split()
        chemicals = {name: int(amount) for amount, name in map(str.split, inputs)}
        reactions[name] = {'creates': int(amount), 'reactants': chemicals}

    ore = ore_for_n_fuel(1, reactions)
    print('p1:', ore)


if __name__ == "__main__":
    main()
