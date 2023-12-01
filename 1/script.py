import sys

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    # that sure was some awkward bullshit for day 1
    m = {'one': 'one1one',
        'two': 'two2two',
        'three': 'three3three',
        'four': 'four4four',
        'five': 'five5five',
        'six': 'six6six',
        'seven': 'seven7seven',
        'eight': 'eight8eight',
        'nine': 'nine9nine'}

    sum = 0
    for i in inputs:
        for word, replace in m.items():
            i = i.replace(word, replace)
        i = ''.join(filter(str.isdigit, i))

        if i:
            i = f'{i[0]}{i[-1]}'
            sum += int(i)

    print(sum)
