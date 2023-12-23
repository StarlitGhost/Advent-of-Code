with open('input') as f:
    buf = f.read().rstrip('\n')

    marker_len = 14
    for idx, _ in enumerate(buf):
        chars = buf[idx:idx+marker_len]
        if len(set(chars)) == marker_len:
            print(chars, idx, idx+marker_len)
            break
