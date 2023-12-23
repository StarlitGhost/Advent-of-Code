import sys
import re

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    def p1_nice(s):
        if any(bad in s for bad in ['ab', 'cd', 'pq', 'xy']):
            #print('bad substr:', s)
            return False
        elif len([v.start() for v in re.finditer(r'[aeiou]', s)]) < 3:
            #print('<3 vowels:', s)
            return False
        elif not re.search(r'(\w)\1', s):
            #print('no repeats:', s)
            return False
        else:
            return True

    def p2_nice(s):
        if not re.search(r'(\w\w)\w*\1', s):
            #print('no pairs:', s)
            return False
        elif not re.search(r'(\w)\w\1', s):
            #print('no x_x:', s)
            return False
        else:
            return True

    p1_sum = sum(1 for s in inputs if p1_nice(s))
    print(p1_sum)

    p2_sum = sum(1 for s in inputs if p2_nice(s))
    print(p2_sum)
