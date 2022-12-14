import sys
import json
import functools

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
    #print(f'{indent_s(indent)}- Compare {str(left).replace(" ", "")} vs {str(right).replace(" ","")}')
    # both numbers
    if not isinstance(left, list) and not isinstance(right, list):
        #print(f'{indent_s(indent+1)}- Compare {left} vs {right}')
        if left > right:
            #print(f'{indent_s(indent+2)}- Right side is smaller, so inputs are not in the right order')
            return 1
        elif left < right:
            #print(f'{indent_s(indent+2)}- Left side is smaller, so inputs are in the right order')
            return -1
        else:
            return 0

    # left number, right list
    elif not isinstance(left, list) and isinstance(right, list):
        #print(f'{indent_s(indent+1)}- Compare {left} vs {str(right).replace(" ","")}')
        #print(f'{indent_s(indent+2)}- Mixed types; convert left to [{left}] and retry comparison')
        return compare([left], right, indent+2)

    # left list, right number
    elif isinstance(left, list) and not isinstance(right, list):
        #print(f'{indent_s(indent+1)}- Compare {str(left).replace(" ","")} vs {right}')
        #print(f'{indent_s(indent+2)}- Mixed types; convert right to [{right}] and retry comparison')
        return compare(left, [right], indent+2)

    # both lists, neither empty
    elif left and right:
        result = compare(left[0], right[0], indent+1)
        if result:
            return result
        else:
            return compare(left[1:], right[1:])

    # both lists, either/both empty
    elif left:
        return 1
    elif right:
        return -1
    else:
        return 0


packets = [[[2]], [[6]]]
valid_pairs = []
for idx, pair in enumerate(pairs):
    one, two = pair
    #print(f'== Pair {idx+1} ==')
    if compare(one, two) in [-1]:
        valid_pairs.append(idx+1)
    print()
    packets += [one, two]

print(f'Valid: {valid_pairs} {sum(valid_pairs)}')

sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))
#for packet in sorted_packets:
#    print(packet)
print((sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1))
