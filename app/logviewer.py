import sys
import pygame
from common import flatten

# print(flatten((None, (1559918512028036058, ((112, (None, (4, (16, None)))), None)))))

def parse_line(line):
    a = eval(line)
    f = flatten(a)
    # print(a, "--f->", f)
    return f

def main():
    outs, ins = [], []
    for line in sys.stdin:
        try:
            if line.startswith("->"):
                outs.append(parse_line(line[3:].strip()))
            if line.startswith("<-"):
                ins.append(parse_line(line[3:].strip()))
        except:
            break

    print(outs)
    print(ins)

if __name__ == "__main__":
    main()
