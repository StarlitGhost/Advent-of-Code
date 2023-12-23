from GhostyUtils import aoc


def gen_next():
    row = top_row = 0
    col = 0
    code = 20151125
    yield code, row, col
    while True:
        code *= 252533
        code %= 33554393
        if row == 0:
            row = top_row + 1
            top_row = row
            col = 0
        else:
            row -= 1
            col += 1
        yield code, row, col


if __name__ == "__main__":
    m_row, m_col = aoc.read().split()[-3::2]
    m_row = int(m_row[:-1])
    m_col = int(m_col[:-1])

    for code_idx, code in enumerate(gen_next()):
        code, row, col = code
        if row == m_row-1 and col == m_col-1:
            print(f'{code} | Code #{code_idx+1}')
            break
