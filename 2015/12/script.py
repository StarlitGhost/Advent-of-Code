import sys
import re
import json
import pprint


def reject_red(obj):
    match obj:
        case list():
            l = []
            for o in obj:
                l.append(reject_red(o))
            return l
        case dict():
            if 'red' in obj.values():
                return {}
            else:
                for k, v in obj.items():
                    obj[k] = reject_red(v)
                return obj
        case _:
            return obj

def sum_numbers(string):
    numbers = re.findall(r'-?\d+', string)
    numbers = [int(n) for n in numbers]
    return sum(numbers)


if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    # p1
    print(sum_numbers(inputs[0]))

    # p2
    j = json.loads(inputs[0])
    j = reject_red(j)
    print(sum_numbers(json.dumps(j)))
