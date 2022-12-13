import sys
import json

inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

pairs = []
while True:
    pair = (json.loads(next(inputs)), json.loads(next(inputs)))
    pairs.append(pair)

    try:
        next(inputs)
    except StopIteration:
        break

def indent_s(level):
    return ' '*level*2

def compare(left, right, indent=0):
    print(f'{indent_s(indent)}- Compare {str(left).replace(" ", "")} vs {str(right).replace(" ","")}')
    for i, l in enumerate(left):
        try:
            # both numbers
            if not isinstance(l, list) and not isinstance(right[i], list):
                print(f'{indent_s(indent+1)}- Compare {l} vs {right[i]}')
                if l > right[i]:
                    print(f'{indent_s(indent+2)}- Right side is smaller, so inputs are not in the right order')
                    return False
                elif l < right[i]:
                    print(f'{indent_s(indent+2)}- Left side is smaller, so inputs are in the right order')
                    return True
                else:
                    continue

            # left number, right list
            elif not isinstance(l, list) and isinstance(right[i], list):
                print(f'{indent_s(indent+1)}- Compare {l} vs {str(right[i]).replace(" ","")}')
                print(f'{indent_s(indent+2)}- Mixed types; convert left to [{l}] and retry comparison')
                result = compare([l], right[i], indent+2)
                if result in [True, False]:
                    return result

            # left list, right number
            elif isinstance(l, list) and not isinstance(right[i], list):
                print(f'{indent_s(indent+1)}- Compare {str(l).replace(" ","")} vs {right[i]}')
                print(f'{indent_s(indent+2)}- Mixed types; convert right to [{right[i]}] and retry comparison')
                result = compare(l, [right[i]], indent+2)
                if result in [True, False]:
                    return result

            # both lists
            else:
                result = compare(l, right[i], indent+1)
                if result in [True, False]:
                    return result

        # right ran out
        except IndexError:
            print(f'{indent_s(indent+1)}- Right side ran out of items, so inputs are not in the right order')
            return False

    if indent == 0:
        print(f'{indent_s(indent+1)}- Left side ran out of items, so inputs are in the right order')
        return True

valid_pairs = []
for idx, pair in enumerate(pairs):
    one, two = pair
    print(f'== Pair {idx+1} ==')
    if compare(one, two):
        valid_pairs.append(idx+1)
    print()

print(f'Valid: {valid_pairs} {sum(valid_pairs)}')
