import sys
import re

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    def nice(s):
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

    nice_strings = sum(1 for s in inputs if nice(s))
    print(nice_strings)
