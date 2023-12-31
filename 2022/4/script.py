with open('input') as f:
    inputs = (line.rstrip('\n') for line in f)

    full_overlaps = 0
    partial_overlaps = 0

    for pair in inputs:
        l, r = pair.split(',')
        ll, lh = map(int, l.split('-'))
        rl, rh = map(int, r.split('-'))
        intervals = sorted([(ll, lh), (rl, rh)], key=lambda rng: rng[1]-rng[0])
        # print(intervals)
        if (intervals[0][0] >= intervals[1][0] and
                intervals[0][1] <= intervals[1][1]):
            # print('full')
            full_overlaps += 1
        if not ((intervals[0][0] > intervals[1][1] and
                 intervals[0][1] > intervals[1][1]) or
                (intervals[0][0] < intervals[1][0] and
                 intervals[0][1] < intervals[1][0])):
            # print('partial')
            partial_overlaps += 1

    print(full_overlaps)
    print(partial_overlaps)
