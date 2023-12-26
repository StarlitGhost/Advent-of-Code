from GhostyUtils import aoc
from collections import Counter
import sys


def main():
    pixels = aoc.read()
    w = 25
    h = 6
    num_layers = len(pixels) // (w * h)

    layers = []
    for l_idx in range(num_layers):
        layer_start = l_idx * w * h
        layer = []
        for i in range(6):
            line = pixels[layer_start + i*w:layer_start + i*w + w]
            layer.append([pix for pix in line])
        layers.append(layer)

    fewest = sys.maxsize
    fewest_layer = 0
    ones, twos = sys.maxsize, sys.maxsize
    for i, layer in enumerate(layers):
        layer = '\n'.join(''.join(line) for line in layer)
        count = Counter(layer)
        del count['\n']
        if count['0'] < fewest:
            fewest = count['0']
            fewest_layer = i
            ones, twos = count['1'], count['2']
#       print(f'####### layer {i+1:03} #######')
#       print(count)
#       print(layer)
#       print()
    print(f'p1: {ones * twos} | layer {fewest_layer}')

    image = layers[0]
    for layer in layers[1:]:
        for y, line in enumerate(layer):
            for x, (i, l) in enumerate(zip(image[y], line)):
                image[y][x] = i if i in '01' else l
    print('\n'.join(''.join(line) for line in image).replace('0', ' ').replace('1', '#'))


if __name__ == "__main__":
    main()
