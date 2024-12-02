from GhostyUtils import aoc


def main():
    inputs = aoc.read_lines()

    safe = 0
    for report in inputs:
        report = [int(r) for r in report.split()]
        diffs = [ln - l for l, ln in zip(report, report[1:])]
        safety = ((all(d < 0 for d in diffs)
                   or all(d > 0 for d in diffs))
                  and all(0 < abs(d) <= 3 for d in diffs))
        if safety:
            safe += 1
        print(diffs, safety)

    print("p1:", safe)


if __name__ == "__main__":
    main()
