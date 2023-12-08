import sys
from collections import defaultdict
import re

if __name__ == '__main__':
    replacements, molecule = open(sys.argv[1]).read().strip().split('\n\n')

    conversions = defaultdict(list)
    for replacement in replacements.split('\n'):
        start, end = replacement.split(' => ')
        conversions[start].append(end)

    unique_molecules = set()
    for original, replacements in conversions.items():
        for token in re.finditer(original, molecule):
            for replace in replacements:
                new_molecule = molecule[:token.start()] + replace + molecule[token.end():]
                unique_molecules.add(new_molecule)
    print(len(unique_molecules))
