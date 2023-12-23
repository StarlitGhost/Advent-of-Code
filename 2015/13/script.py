import sys
import itertools
from pprint import pprint


def build_tables(relationships):
    people = list(relationships.keys())
    return [[people[0]] + list(l) for l in itertools.permutations(people[1:])]

def score(table, relationships):
    score = 0
    for pos, person in enumerate(table):
        score += relationships[person][table[pos-1]]
        if pos+1 < len(table):
            score += relationships[person][table[pos+1]]
        else:
            score += relationships[person][table[0]]
    return score

def highest_score(tables, relationships):
    high_score = 0
    high_table = []
    for table in tables:
        table_score = score(table, relationships)
        if table_score > high_score:
            high_score = table_score
            high_table = table
    return high_score, high_table


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    relationships = {}

    for line in inputs:
        person, next_to = line.split(' happiness units by sitting next to ')
        next_to = next_to[:-1]
        person, happy = person.split(' would ')
        change, happy = happy.split()
        happy = int(happy) if change == 'gain' else -int(happy)

        if person not in relationships:
            relationships[person] = {}
        relationships[person][next_to] = happy

    # p1
    tables = build_tables(relationships)
    high_score, high_table = highest_score(tables, relationships)
    print(high_score, high_table)

    # p2
    relationships['Ghosty'] = {}
    for person in relationships.keys():
        relationships['Ghosty'][person] = 0
        relationships[person]['Ghosty'] = 0
    tables = build_tables(relationships)
    high_score, high_table = highest_score(tables, relationships)
    print(high_score, high_table)
