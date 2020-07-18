import sys

sys.setrecursionlimit(123456)
values = {}
cache = {}

def evaluated(sym, arg=None):
    # print(sym, end="...")
    # sys.stdout.flush()
    if arg is None:
        if sym not in cache:
            cache[sym] = values[sym]()
        return cache[sym]
    else:
        key = (sym, str(arg))
        if key not in cache:
            cache[key] = Ap(values[sym], arg)()
        return cache[key]


class Symbol(object):
    def __init__(self, key):
        self.key = key

    def __call__(self, x=None):
        if x is None:
            return evaluated(self.key)
            # return values[self.key]()
        #while isinstance(x, Ap):
        #    x = x()
        #if isinstance(x, Number):
        #    return evaluated(self.key, x.val)
        return evaluated(self.key, x)
        return Ap(values[self.key], x)()

    def __repr__(self):
        return self.key


class Cons(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(Ap(x, self.val[0]), self.val[1])()
        # return Cons(self.val + [x() if isinstance(x, Ap) else x])
        return Cons(self.val + [x])

    def __repr__(self):
        return str(self.val)


class Neg(object):
    def __call__(self, x):
        return -x()

    def __repr__(self):
        return "Neg"


class C(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(Ap(self.val[0], x), self.val[1])()
        return C(self.val + [x])

    def __repr__(self):
        return "C({0})".format(",".join(map(str, self.val))) if self.val else "C"


class B(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(self.val[0], Ap(self.val[1], x))()

        return B(self.val + [x])

    def __repr__(self):
        return "B({0})".format(",".join(map(str, self.val))) if self.val else "B"


class S(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(Ap(self.val[0], x), Ap(self.val[1], x))()
        return S(self.val + [x])

    def __repr__(self):
        return "S({0})".format(",".join(map(str, self.val))) if self.val else "S"


class IsNil(object):
    def __call__(self, x):
        while isinstance(x, Ap) or isinstance(x, Symbol):
            x = x()
        assert(isinstance(x, Cons) or isinstance(x, Nil))
        if isinstance(x, Nil):
            return T()
        else:
            return F()

    def __repr__(self):
        return "IsNil"


class Car(object):
    def __call__(self, x):
        # if len(self.val) == 1:
        #     return self.val[0]()
        while isinstance(x, Ap) or isinstance(x, Symbol):
            x = x()
        if not isinstance(x, Cons):
            print(x)
            print(type(x))
        assert isinstance(x, Cons)
        return x.val[0]()

    def __repr__(self):
        return "Car"


class Cdr(object):
    def __call__(self, x):
        # if len(self.val) == 1:
        #     return x()
        while isinstance(x, Ap) or isinstance(x, Symbol):
            x = x()
        if not isinstance(x, Cons):
            print(x)
            print(type(x))
        assert isinstance(x, Cons)
        return x.val[1]()

    def __repr__(self):
        return "Cdr"


class Add(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() + x()
        return Add(self.val + [x])

    def __repr__(self):
        return "Add({0})".format(",".join(map(str, self.val))) if self.val else "Add"


class Mul(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() * x()
        return Mul(self.val + [x])

    def __repr__(self):
        return "Mul({0})".format(",".join(map(str, self.val))) if self.val else "Mul"


class Div(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() // x()
        return Div(self.val + [x])

    def __repr__(self):
        return "Div({0})".format(",".join(map(str, self.val))) if self.val else "Div"


class T(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]()
        return T(self.val + [x])

    def __repr__(self):
        return "T({0})".format(",".join(map(str, self.val))) if self.val else "T"


class F(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            return x()
        return F(self.val + [x])

    def __repr__(self):
        return "F({0})".format(",".join(map(str, self.val))) if self.val else "F"


class Lt(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            a = self.val[0]()
            b = x()
            assert(isinstance(a, Number))
            assert(isinstance(b, Number))
            if a.val < b.val:
                return T()
            else:
                return F()
        return Lt(self.val + [x])

    def __repr__(self):
        return "Lt({0})".format(",".join(map(str, self.val))) if self.val else "Lt"


class Eq(object):
    def __init__(self, val=[]):
        self.val = list(val)

    def __call__(self, x):
        if len(self.val) == 1:
            a = self.val[0]()
            b = x()
            #print(a, type(a))
            #print(b, type(b))
            assert(isinstance(a, Number))
            assert(isinstance(b, Number))
            if a.val == b.val:
                return T()
            else:
                return F()
        return Eq(self.val + [x])

    def __repr__(self):
        return "Eq({0})".format(",".join(map(str, self.val))) if self.val else "Eq"


class I(object):
    def __call__(self, x):
        return x

    def __repr__(self):
        return "I"


class Nil(object):
    def __call__(self):
        return self

    def __repr__(self):
        return "nil"

SH = 0
LIM = 0

class Ap(object):
    def __init__(self, a, b):
        self.first = a
        self.second = b
        self.res = None

    def __call__(self):
        if self.res is not None:
            return self.res
        global SH, LIM
        if SH < LIM:
            print(" " * SH, self) # , ":", self.first, self.second)
        #print("sf:", type(self.first))
        #print("sc:", type(self.second))
        SH += 2
        arg = self.second
        f = self.first
        #print("f:", f)
        #print("type f:", type(f))
        #print("arg:", arg)
        #print("type arg:", type(arg))
        while isinstance(f, Ap):
            f = f()

        res = f(arg)

        while isinstance(res, Ap):
            res = res()
        SH -= 2
        if SH < LIM:
            print(" " * SH, "!!! result:", res)
        self.res = res
        return res

    def __str__(self):
        return str(self.first) + "(" + str(self.second) + ")"


class Number(object):
    def __init__(self, val):
        self.val = val

    def __call__(self):
        return self

    def __repr__(self):
        return str(self.val)

    def __add__(self, other):
        return Number(self.val + other.val)

    def __mul__(self, other):
        return Number(self.val * other.val)

    def __floordiv__(self, other):
        return Number(self.val // other.val)

    def __neg__(self):
        return Number(-self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __neq__(self, other):
        return self.val != other.val

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val



def unroll(x):
    if isinstance(x, Number) or isinstance(x, Nil):
        return x
    if isinstance(x, Ap):
        return unroll(x())
    if isinstance(x, Cons):
        return Cons()(unroll(x.val[0]()))(unroll(x.val[1]()))

    print("x:", x, ", type:", type(x))
    fail

def mod_num(num):
    if num == 0:
        return "010"

    m = abs(num)
    sgn = "01" if num > 0 else "10"
    for sz in range(1, 10 ** 9):
        if 2 ** (4 * sz) > m:
            return sgn + ("1" * sz) + "0" + bin(m)[2:].zfill(4 * sz)

assert mod_num(16) == "0111000010000"
assert mod_num(-16) == "1011000010000"
assert mod_num(2) == "01100010"
assert mod_num(-2) == "10100010"

def mod(x):
    """
    if isinstance(x, Nil):
        return "(00)"
    if isinstance(x, Number):
        return mod_num(x.val)
    if isinstance(x, Cons):
        return "(11|" + mod(x.val[0]) + "|" + mod(x.val[1]) + ")"
    """
    if isinstance(x, Nil):
        return "00"
    if isinstance(x, Number):
        return mod_num(x.val)
    if isinstance(x, Cons):
        return "11" + mod(x.val[0]) + mod(x.val[1])

    fail


def modem(x):
    print("Will call modem", x)
    res = unroll(x)
    print("unrolled:", res)
    rm = mod(res)
    print("modulated:", rm)
    return x


def send(x):
    print("Will send", x, type(x))
    res = unroll(x)
    print("unrolled:", res)
    rm = mod(res)
    print("modulated:", rm)
    raise x

def multipledraw(x):
    print("Multiple draw", unroll(x))

"""
ap ap f38 x2 x0 = ap ap ap if0 ap car x0 ( ap modem ap car ap cdr x0 , ap multipledraw ap car ap cdr ap cdr x0 ) |ap ap ap interact x2 |ap modem ap car ap cdr x0| |ap send ap car ap cdr ap cdr x0||
ap ap ap interact x2 x4 x3 = ap ap f38 x2 ap ap x2 x4 x3
"""
def f38(x2, x0):
    print("Call f38", x2, x0)
    a = Car()(x0)
    print("a:", a, ",type:", type(a))
    assert(isinstance(a, Number))
    if a.val == 0:
        print("a.val is 0")
        first = modem(Car()(Cdr()(x0)))
        print("first done")
        second = multipledraw(Car()(Cdr()(Cdr()(x0))))
        print("second done")
        #return Cons()(first)(Cons()(second)(Nil()))
        return Cons()(first)(second)
    else:
        print("a.val is not 0")
        rm = modem(Car()(Cdr()(x0)))
        print("modem done")
        rs = send(Car()(Cdr()(Cdr()(x0))))
        print("send done")
        interact(x2, rm, rs)


def interact(x2, x4, x3):
    print("Run interact with", x2, x4, x3)
    return f38(x2, Ap(Ap(x2, x4), x3)())



def parse(tokens, shift):
    # print(" " * (shift * 4), " ".join(tokens))

    cur, tokens = tokens[0], tokens[1:]
    if cur[0] == ":":
        return Symbol(cur), tokens

    if cur == "ap":
        first, tokens = parse(tokens, shift + 1)
        second, tokens = parse(tokens, shift + 1)
        return Ap(first, second), tokens

    if cur == "cons":
        return Cons(), tokens

    try:
        x = int(cur)
        return Number(x), tokens
    except:
        pass

    if cur == "nil":
        return Nil(), tokens

    if cur == "neg":
        return Neg(), tokens

    if cur == "c":
        return C(), tokens

    if cur == "b":
        return B(), tokens

    if cur == "s":
        return S(), tokens

    if cur == "isnil":
        return IsNil(), tokens

    if cur == "car":
        return Car(), tokens

    if cur == "cdr":
        return Cdr(), tokens

    if cur == "eq":
        return Eq(), tokens

    if cur == "lt":
        return Lt(), tokens

    if cur == "add":
        return Add(), tokens

    if cur == "mul":
        return Mul(), tokens

    if cur == "div":
        return Div(), tokens

    if cur == "i":
        return I(), tokens

    if cur == "t":
        return T(), tokens

    print("Parse failed on: '{0}'".format(cur))
    assert False

for line in sys.stdin:
    first, last = line.strip().split("=")
    first = first.strip()
    values[first] = parse(last.strip().split(), 0)[0]

print("Parsing {0} entites ok".format(len(values)))

for v in values:
    print(v, end=" = ")
    #sys.stderr.write(v)
    sys.stdout.flush()
    print(evaluated(v))

res = Nil()
cnt = 0
while True:
    res = interact(evaluated("galaxy"), res, Cons()(Number(0))(Number(0)))
    sys.stderr.write(str(res))
    sys.stderr.flush()
    cnt += 1
    res = res.val[0]
