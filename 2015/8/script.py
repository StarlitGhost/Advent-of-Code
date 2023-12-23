import sys

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    lit_len = 0
    mem_len = 0
    esc_len = 0
    for string in inputs:
        lit_len += len(string)
        # big cheats
        unescaped = bytes(string[1:-1], "utf-8").decode("unicode_escape")
        mem_len += len(unescaped)
        # even bigger cheats
        escaped = repr(string)
        esc_len += len(escaped) + escaped.count('"')
        #print(string, len(string), '#', unescaped, len(unescaped), '#', escaped, len(escaped) + escaped.count('"'))

    print(lit_len - mem_len)
    print(esc_len - lit_len)
