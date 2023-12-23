from collections import OrderedDict
from GhostyUtils import aoc


def ascii_hash(string):
    v = 0
    for c in string:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def handle_lens(step, boxes):
    if '=' in step:
        label = step[:-2]
        box = ascii_hash(label)
        lens = int(step[-1])
        boxes[box][label] = lens
    elif step.endswith('-'):
        label = step[:-1]
        box = ascii_hash(label)
        if label in boxes[box]:
            boxes[box].pop(label)


if __name__ == '__main__':
    steps = aoc.read().split(',')

    print(sum(ascii_hash(step) for step in steps))

    boxes = [OrderedDict() for _ in range(256)]
    for step in steps:
        handle_lens(step, boxes)

    focusing_power = 0
    for box_id, box in enumerate(boxes):
        for slot_id, focal_length in enumerate(box.values()):
            focusing_power += (box_id + 1) * (slot_id + 1) * focal_length
    print(focusing_power)
