import sys
from collections import Counter


def type_rank(cards):
    c = Counter(card for card in cards)
    match sorted(c.values(), reverse=True):
        case [5]:
            return 6
        case [4,1]:
            return 5
        case [3,2]:
            return 4
        case [3,1,1]:
            return 3
        case [2,2,1]:
            return 2
        case [2,1,1,1]:
            return 1
        case [1,1,1,1,1]:
            return 0

def convert_card(card):
    return '23456789TJQKA'.index(card)

def rank_hand(hand):
    rank = [type_rank(hand['cards'])] + [convert_card(card) for card in hand['cards']]

    #print(hand['cards'], rank)
    
    return rank


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    hands = [{'cards': line[0], 'bet': int(line[1])} for line in map(str.split, inputs)]
    hands.sort(key=rank_hand)
    #print(hands)

    print(sum((i+1)*hand['bet'] for i, hand in enumerate(hands)))
