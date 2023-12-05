import sys
import functools
from pprint import pprint


class Ingredient:
    def __init__(self, string):
        self.name, properties = string.split(': ')
        self.props = {}
        for prop in properties.split(', '):
            name, amount = prop.split()
            self.props[name] = int(amount)

    def __repr__(self):
        return str(self.__dict__)


def combinations(total, elements):
    if elements < 1:
        return []
    if elements == 1:
        return [[total]]
    if elements == 2:
        return [[i,total-i] for i in range(1, total-elements+2)]
    return [l[:-1] + ab for l in combinations(total, elements-1) for ab in combinations(l[-1], 2)]

def score_combo(ingredients, combo):
    props = {}
    for i, teaspoons in enumerate(combo):
        for name, amount in ingredients[i].props.items():
            if name not in props:
                props[name] = 0
            props[name] += teaspoons * amount

    for name, total in props.items():
        if total < 0:
            props[name] = 0

    score = functools.reduce(lambda x, y: x*y, list(props.values())[:-1])
    #print(score, props)
    return score, props

def find_best_ratio(ingredients, total_teaspoons, calories=False):
    combos = combinations(total_teaspoons, len(ingredients))
    highscore = 0
    high_combo = []
    for combo in combos:
        score, props = score_combo(ingredients, combo)
        if calories and props['calories'] != 500:
            continue
        if score > highscore:
            highscore = score
            high_combo = combo
    return highscore, high_combo


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    ingredients = [Ingredient(line) for line in inputs]

    # p1
    highscore, high_combo = find_best_ratio(ingredients, 100, False)
    print(highscore, {ingredients[i].name: v for i, v in enumerate(high_combo)})

    # p2
    highscore, high_combo = find_best_ratio(ingredients, 100, True)
    print(highscore, {ingredients[i].name: v for i, v in enumerate(high_combo)})
