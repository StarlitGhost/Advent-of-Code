import sys
from pprint import pprint

def solve(groups, remaining_length, record):
    if not groups:
        #return ['.'*remaining_length]
        return ['']
    if groups[0] > remaining_length:
        print(f"group won't fit!")
        raise Exception

    max_start = remaining_length - sum(groups) - (len(groups)-1)
    record_offset = len(record)-remaining_length

    arrangements = []
    for i in range(max_start+1):
        if '.' in record[record_offset+i:record_offset+i+groups[0]]:
            continue
        if len(groups) > 1 and record[record_offset+i+groups[0]] == '#':
            continue
        if record_offset+i > 0 and record[record_offset+i-1] == '#':
            continue
        for arr in solve(groups[1:], remaining_length-i-groups[0]-1, record):
            arrangement = '.'*i+'#'*groups[0]+('.' if len(groups) > 1 else '.'*(max_start-i))
            if validate_solution(record, arrangement[i:], record_offset+i):
                arrangements.append(arrangement+arr)
    return arrangements

def solutions(record, groups):
    size = len(record)
    sols = solve(groups, size, record)
    sols = [sol for sol in sols if validate_solution(record, sol)]
    return sols

def validate_solution(record, solution, record_offset=0):
    if len(solution) > len(record) - record_offset:
        return False
    for r, s in zip(record[record_offset:record_offset+len(solution)], solution):
        if r == '?':
            continue
        if s != r:
            return False
    return True 

def count_solutions(sols, record):
    return sum(1 for s in sols if validate_solution(record, s))

def unfold(springs):
    for record, groups in springs:
        yield ['?'.join(record for _ in range(5)), groups * 5]

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1] if len(sys.argv) >= 2 else 'example')]

    springs = []
    for line in inputs:
        record, groups = line.split()
        groups = list(map(int, groups.split(',')))
        springs.append([record, groups])

    total_sols = 0
    for spring in springs:
        sols = solutions(spring[0], spring[1])
        total_sols += count_solutions(sols, spring[0])
    print(total_sols)

    total_sols = 0
    for spring in unfold(springs):
        sols = solutions(spring[0], spring[1])
        total_sols += count_solutions(sols, spring[0])
    print(total_sols)
