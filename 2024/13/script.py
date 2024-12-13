from GhostyUtils import aoc
from GhostyUtils.vec2 import Vec2


def solve(machine: list[list[tuple], tuple], offset: int = 0):
    a, b = [Vec2(button) for button in machine[0]]
    p = Vec2(machine[1]) + Vec2(offset, offset)

    if aoc.args.progress or aoc.args.verbose:
        print(f"A vec: {a}, B vec: {b}, Prize location: {p}")

    det = (a.x * b.y - a.y * b.x)

    a_presses = int((p.x * b.y - p.y * b.x) / det)
    b_presses = int((p.y * a.x - p.x * a.y) / det)

    if a * a_presses + b * b_presses == p:
        if aoc.args.progress or aoc.args.verbose:
            print(f"> A: {a_presses}x, B: {b_presses}x, Tokens: {a_presses * 3 + b_presses}")
        return a_presses * 3 + b_presses
    else:
        if aoc.args.progress or aoc.args.verbose:
            print("> Misses")
        return 0


def main():
    inputs = aoc.read_sections()

    machines = []
    for mch in inputs:
        mch = mch.splitlines()
        buttons = [tuple(int(coord[2:])
                         for coord in btn.split(': ')[1].split(', '))
                   for btn in mch[:2]]
        prize = tuple(int(coord[2:]) for coord in mch[2].split(': ')[1].split(', '))

        machines.append([buttons, prize])

        if aoc.args.verbose:
            print(f"buttons: {buttons}, prize: {prize}")

    print(f"p1: {sum(solve(machine) for machine in machines)}")
    print(f"p2: {sum(solve(machine, offset=10000000000000) for machine in machines)}")


if __name__ == "__main__":
    main()
