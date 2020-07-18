import sys
import pygame


def flatten(a):
    if not isinstance(a, list) and not isinstance(a, tuple):
        return [a] if a is not None else []

    if len(a) == 2:
        if isinstance(a[0], list) or isinstance(a[0], tuple):
            res = flatten(a[0])
        else:
            res = a[0]
        res = [res] + flatten(a[1])
        # print("flatten {}: got {}".format(a, res))
        return res

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
