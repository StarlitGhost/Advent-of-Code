hand_scores = {
    'X': 1, # rock
    'Y': 2, # paper
    'Z': 3, # scissors
    'A': 1,
    'B': 2,
    'C': 3,
    }

loss = 0
draw = 3
win = 6


def part1():
    wins = ['A Y', 'B Z', 'C X']
    draws = ['A X', 'B Y', 'C Z']
    losses = ['A Z', 'B X', 'C Y']

    score = 0

    def hand_score(hand, outcome):
        #print(hand, hand_scores[hand.split()[1]], outcome)
        return hand_scores[hand.split()[1]] + outcome

    with open('input') as f:
        inputs = [line.rstrip('\n') for line in f]
        for hand in inputs:
            if hand in wins:
                score += hand_score(hand, win)
            elif hand in draws:
                score += hand_score(hand, draw)
            else:
                score += hand_score(hand, loss)
        print(score)


def part2():
    def hand_score(op_hand, outcome):
        my_hand = (hand_scores[op_hand] - 1 + {'X': -1, 'Y': 0, 'Z': 1}[outcome]) % 3 + 1
        score = {'X': 0, 'Y': 3, 'Z': 6}[outcome]
        #print(op_hand, outcome, my_hand, score)
        return my_hand + score

    score = 0

    with open('input') as f:
        inputs = [line.rstrip('\n') for line in f]
        for hand in inputs:
            op_hand, outcome = hand.split()
            score += hand_score(op_hand, outcome)
        print(score)


part1()
part2()
