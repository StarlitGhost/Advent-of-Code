from GhostyUtils import aoc


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
    print(total)
