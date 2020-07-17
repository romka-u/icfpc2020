import sys


def parse_int(s):
    sz = 0
    while s[0] == "1":
        sz += 1
        s = s[1:]
    s = s[1:]
    bits = 4 * sz
    if bits == 0:
        return 0, s
    return int(s[:bits], 2), s[bits:]

def dem(s):
    print("dem", s)
    assert len(s) >= 2
    if s[:2] == "01":
        x, s = parse_int(s[2:])
        return x, s

    if s[:2] == "11":
        s = s[2:]
        x, s = dem(s)
        y, s = dem(s)
        if y == None:
            return x, s
        return (x, y), s

    if s[:2] == "00":
        return None, s[2:]
    assert False

for line in sys.stdin:
    r = dem(line.strip())
    print(r[0])
