import sys

def mod(num):
    if num == 0:
        return "010"
    for sz in range(1, 10 ** 9):
        if 2 ** (4 * sz) > num:
            return "01" + ("1" * sz) + "0" + bin(num)[2:].zfill(4 * sz)

assert mod(5) == "01100101"

a = [1, 2, 3]

s = ""
for x in a:
    s += "11" + mod(x)
s += "00"

print(s)


