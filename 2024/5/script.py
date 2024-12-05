from GhostyUtils import aoc
from collections import defaultdict


def validate(page_order, rule_map) -> bool:
    for i, page in enumerate(page_order):
        if not all(page not in rule_map[other_page] for other_page in page_order[i+1:]):
            return False
    return True


def find_middle(page_order, rule_map) -> int:
    for page in page_order:
        pages = rule_map[page].intersection(set(page_order))
        if len(pages) == len(page_order)//2:
            return page
        # print(page_order, page, rule_map[page], pages)


def main():
    rules, page_orders = aoc.read_sections()
    rules = [list(map(int, rule.split('|'))) for rule in rules.split('\n')]
    page_orders = [list(map(int, pages.split(','))) for pages in page_orders.split('\n')]
    rule_map = defaultdict(set)
    for rule in rules:
        rule_map[rule[0]].add(rule[1])

    print("p1:", sum(page_order[len(page_order)//2]
                     for page_order in page_orders
                     if validate(page_order, rule_map)))

    print("p2:", sum(find_middle(page_order, rule_map)
                     for page_order in page_orders
                     if not validate(page_order, rule_map)))


if __name__ == "__main__":
    main()
