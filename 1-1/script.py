import heapq

if __name__ == '__main__':
    elves = [0]
    with open('input') as inputs:
        for i in inputs:
            if i.strip():
                elves[-1] += int(i)
            else:
                elves.append(0)
        print(max(elves))
        print(sum(heapq.nlargest(3, elves)))
