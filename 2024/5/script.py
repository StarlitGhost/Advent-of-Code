from GhostyUtils import aoc
from collections import defaultdict


def validate(page_order, rule_map) -> bool:
    for i, page in enumerate(page_order):
        if not all(page not in rule_map[other_page] for other_page in page_order[i+1:]):
            return False
    return True


def main():
    rules, page_orders = aoc.read_sections()
    rules = [list(map(int, rule.split('|'))) for rule in rules.split('\n')]
    page_orders = [list(map(int, pages.split(','))) for pages in page_orders.split('\n')]
    rule_map = defaultdict(list)
    for rule in rules:
        rule_map[rule[0]].append(rule[1])

    print("p1:", sum(page_order[len(page_order)//2]
                     for page_order in page_orders
                     if validate(page_order, rule_map)))


if __name__ == "__main__":
    main()
