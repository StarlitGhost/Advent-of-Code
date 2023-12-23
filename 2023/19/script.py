from GhostyUtils import aoc
import math


def process_workflow(workflow, part):
    for rule in workflow:
        if ':' in rule:
            cmp, dest = rule.split(':')
            if '<' in rule:
                prop, val = cmp.split('<')
                if part[prop] < int(val):
                    return dest
                else:
                    continue
            if '>' in rule:
                prop, val = cmp.split('>')
                if part[prop] > int(val):
                    return dest
                else:
                    continue
        else:
            return rule


def calc_ranges(name: str, workflows: dict, ranges: dict, accepted: list):
    w_name = name.split('.')[-1]
    # print(w_name, ranges)
    for rule in workflows[w_name]:
        if ':' in rule:
            cmp, dest = rule.split(':')
            if '<' in cmp:
                prop, val = cmp.split('<')
                true_ranges = ranges.copy()
                false_ranges = ranges.copy()
                true_ranges[prop] = (true_ranges[prop][0], int(val)-1)
                false_ranges[prop] = (int(val), false_ranges[prop][1])
            if '>' in cmp:
                prop, val = cmp.split('>')
                true_ranges = ranges.copy()
                false_ranges = ranges.copy()
                true_ranges[prop] = (int(val)+1, true_ranges[prop][1])
                false_ranges[prop] = (false_ranges[prop][0], int(val))
            if dest == 'A':
                true_ranges['combos'] = math.prod(v[1]-v[0]+1 for v in true_ranges.values())
                # print('A', true_ranges)
                accepted.append(true_ranges)
                ranges = false_ranges
                continue
            if dest == 'R':
                # print('R', true_ranges)
                ranges = false_ranges
                continue
            calc_ranges(f'{name}.{dest}', workflows, true_ranges, accepted)
            ranges = false_ranges
        else:
            if rule == 'A':
                ranges['combos'] = math.prod(v[1]-v[0]+1 for v in ranges.values())
                # print('A', ranges)
                accepted.append(ranges)
                continue
            if rule == 'R':
                # print('R', ranges)
                continue
            calc_ranges(f'{name}.{rule}', workflows, ranges, accepted)


if __name__ == "__main__":
    workflows_txt, parts_txt = aoc.read_sections()

    parts = []
    for part_txt in parts_txt.splitlines():
        part = {}
        for prop in part_txt[1:-1].split(','):
            name, value = prop.split('=')
            part[name] = int(value)
        parts.append(part)

    workflows = {}
    for workflow_txt in workflows_txt.splitlines():
        name, workflow = workflow_txt.split('{')
        workflow = workflow[:-1].split(',')
        workflows[name] = workflow

    accepted = []
    for part in parts:
        workflow = 'in'
        while True:
            result = process_workflow(workflows[workflow], part)
            if result == 'R':
                break
            elif result == 'A':
                accepted.append(part)
                break
            else:
                workflow = result

    total = 0
    for part in accepted:
        for prop in 'xmas':
            total += part[prop]
    print('p1', total)

    MIN = 1
    MAX = 4000
    ranges = {'x': (MIN, MAX), 'm': (MIN, MAX), 'a': (MIN, MAX), 's': (MIN, MAX)}
    accepted = []
    calc_ranges('in', workflows, ranges, accepted)
    total = sum(a['combos'] for a in accepted)
    print('p2', total)
