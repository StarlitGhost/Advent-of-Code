from GhostyUtils import aoc

if __name__ == '__main__':
    inputs = aoc.read_lines()

    num_cards = len(inputs)
    total = 0
    copies = {n+1: 1 for n in range(num_cards)}

    for num, card in enumerate(inputs):
        win, have = card.split(' | ')
        win = win.split(': ')[1].split()
        have = have.split()

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
