import sys

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    # that sure was some awkward bullshit for day 1
    m = {'one': 'o1ne',
        'two': 't2wo',
        'three': 't3hree',
        'four': 'f4our',
        'five': 'f5ive',
        'six': 's6ix',
        'seven': 's7even',
        'eight': 'e8ight',
        'nine': 'n9ine'}

    sum = 0
    for i in inputs:
        for word, replace in m.items():
            i = i.replace(word, replace)
        i = ''.join(filter(str.isdigit, i))

        if i:
            i = f'{i[0]}{i[-1]}'
            sum += int(i)

    print(sum)
