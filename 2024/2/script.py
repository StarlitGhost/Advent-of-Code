from GhostyUtils import aoc


def is_safe(report) -> True:
    diffs = [ln - l for l, ln in zip(report, report[1:])]
    safety = ((all(d < 0 for d in diffs)
               or all(d > 0 for d in diffs))
              and all(0 < abs(d) <= 3 for d in diffs))
    # print(diffs, safety)
    return safety


def main():
    inputs = aoc.read_lines()

    reports = [[int(r) for r in report.split()] for report in inputs]
    num_safe = sum(1 for report in reports if is_safe(report))

    print("p1:", num_safe)

    num_safe = sum(1 for report in reports
                   if any(is_safe(report[:drop] + report[drop+1:])
                          for drop in range(len(report))))
    print("p2:", num_safe)


if __name__ == "__main__":
    main()
