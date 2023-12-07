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
            c[sorted(c, key=c.get)[-1]] += j

    match sorted(c.values(), reverse=True):
        case [5]: # five of a kind
            return 6
        case [4,1]: # four of a kind
            return 5
        case [3,2]: # full house
            return 4
        case [3,1,1]: # three of a kind
            return 3
        case [2,2,1]: # two pair
            return 2
        case [2,1,1,1]: # one pair
            return 1
        case [1,1,1,1,1]: # high card
            return 0

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
