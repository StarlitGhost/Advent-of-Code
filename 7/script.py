import sys
from collections import Counter


def type_rank(cards, jokers=False):
    c = Counter(card for card in cards)

    if jokers and 'J' in cards:
        max_card = max(c, key=c.get)
        if max_card != 'J':
            # add the number of Js to the highest card count, and delete the count of Js
            c[max_card] += c['J']
            del c['J']
        elif c['J'] < 5:
            # the max card count *is* J, so add to the second highest count instead
            j = c['J']
            del c['J']
            c[max(c, key=c.get)] += j

    return [[1,1,1,1,1],
            [2,1,1,1],
            [2,2,1],
            [3,1,1],
            [3,2],
            [4,1],
            [5]].index(sorted(c.values(), reverse=True))

def convert_card(card):
    return '23456789TJQKA'.index(card)

def convert_card_joker(card):
    return 'J23456789TQKA'.index(card)

def rank_hand(hand):
    # returns [type, c1, c2, c3, c4, c5]
    rank = [type_rank(hand['cards'])] + [convert_card(card) for card in hand['cards']]
    #print(hand['cards'], rank)
    return rank

def rank_hand_jokers(hand):
    # returns [type, c1, c2, c3, c4, c5]
    rank = [type_rank(hand['cards'], jokers=True)] + [convert_card_joker(card) for card in hand['cards']]
    #print(hand['cards'], rank)
    return rank


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    hands = [{'cards': line[0], 'bet': int(line[1])} for line in map(str.split, inputs)]

    hands.sort(key=rank_hand)
    print(sum((i+1)*hand['bet'] for i, hand in enumerate(hands)))

    hands.sort(key=rank_hand_jokers)
    print(sum((i+1)*hand['bet'] for i, hand in enumerate(hands)))
