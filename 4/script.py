import sys
import re

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    num_cards = len(inputs)
    total = 0
    copies = {n+1: 1 for n in range(num_cards)}

    for num, card in enumerate(inputs):
        win, have = card.split(' | ')
        win = re.split(r'\s+', win.split(': ')[1])
        win = [w for w in win if w]
        have = re.split(r'\s+', have)
        have = [h for h in have if h]

        # p1
        score = 0
        for h in have:
            if h in win:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        total += score

        # p2
        matches = 0
        for h in have:
            if h in win:
                matches += 1
        for i in range(1, matches+1):
            if num+1+i in copies:
                copies[num+1+i] += copies[num+1]

    print(total)
    print(sum(copies.values()))
