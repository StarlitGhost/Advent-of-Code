import sys
import hashlib

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))
    inputs = next(inputs)

    # p1
    num = 0
    while True:
        i = f"{inputs}{num}"
        h = hashlib.md5(i.encode("utf-8")).hexdigest()

        if not h.startswith('0'*5):
            num += 1
        else:
            break
    print(num)

    # p2
    while True:
        i = f"{inputs}{num}"
        h = hashlib.md5(i.encode("utf-8")).hexdigest()

        if not h.startswith('0'*6):
            num += 1
        else:
            break
    print(num)
