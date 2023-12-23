import sys
import re


if __name__ == '__main__':
    replacements, molecule = open(sys.argv[1]).read().strip().split('\n\n')

    conversions = {}
    for replacement in replacements.split('\n'):
        start, end = replacement.split(' => ')
        conversions[end] = start

    unique_molecules = set()
    for replacement, original in conversions.items():
        for token in re.finditer(original, molecule):
            new_molecule = molecule[:token.start()] + replacement + molecule[token.end():]
            unique_molecules.add(new_molecule)
    print(len(unique_molecules))

    def conversion_steps(molecule, steps=0):
        if molecule == "e":
            return steps

        # generate all the possible molecules the current molecule could become
        possible_steps = set()
        for original, replacement in conversions.items():
            for token in re.finditer(original, molecule):
                possible_steps.add(molecule[:token.start()] + replacement + molecule[token.end():])

        # sort so we check the largest length reductions first
        possible_steps = sorted(sorted(possible_steps, reverse=True), key=len)

        while possible_steps:
            # recurse and try each of the steps until we find the right path to e
            return conversion_steps(possible_steps.pop(0), steps + 1)
        return None

    print(conversion_steps(molecule))
