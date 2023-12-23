import sys
import re


class password:
    def __init__(self, pw):
        self.pw = [ord(c)-ord('a') for c in pw]

        # validation
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        self._runs = list(''.join(run) for run in zip(alpha, alpha[1:], alpha[2:]))
        self._bad = [ord(c)-ord('a') for c in 'iol']

    def increment(self):
        carry = True
        p = 1
        while carry:
            self.pw[-p] += 1
            if self.pw[-p] == 26:
                self.pw[-p] = 0
                p += 1
            else:
                carry = False
        return self.pw

    def __str__(self):
        return ''.join(chr(ord('a')+c) for c in self.pw)

    def validate(self):
        if any(c in self.pw for c in self._bad):
            #print(self, 'rejected: contains iol')
            return False

        if not any(r in str(self) for r in self._runs):
            #print(self, 'rejected: no runs')
            return False

        if not re.search(r'([a-z])\1.*([a-z])\2', str(self)):
            #print(self, 'rejected: not eough pairs')
            return False

        print(self, 'valid!')
        return True


if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    # p1
    pw = password(inputs[0])
    while not pw.validate():
        pw.increment()

    # p2
    pw.increment()
    while not pw.validate():
        pw.increment()
