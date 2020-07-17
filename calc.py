import sys

sys.setrecursionlimit(12345)
values = {}
cache = {}
LAZY = True

def evaluated(sym):
    # print(sym, end="...")
    # sys.stdout.flush()
    if sym not in cache:
        cache[sym] = values[sym]()
    return cache[sym]


def to_list(a):
    global LAZY
    while isinstance(a, Ap) and not LAZY:
        a = a()
    try:
        return list(a)
    except:
        return [a]


class Symbol(object):
    def __init__(self, key):
        self.key = key

    def __call__(self, x=None):
        if LAZY:
            if x is None:
                return self
            return Symbol("{0}({1})".format(self.key, x))

        if x is None:
            return self
        return Ap(values[self.key], x)()

    def __repr__(self):
        return self.key


class Cons(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return Cons(self.val + [x])

    def __repr__(self):
        return str(self.val)


class Neg(object):
    def __init__(self):
        pass

    def __call__(self, x=None):
        if x is None:
            return self
        return -x


class C(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None, y=None):
        if x is None:
            return self
        if len(self.val) == 2 and not LAZY:
            return Ap(Ap(self.val[0], x), self.val[1])

        if y is not None:
            return C(self.val + [x, y])
        return C(self.val + [x])

    def __repr__(self):
        return "C({0})".format(",".join(map(str, self.val)))


class B(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None, y=None):
        if x is None:
            return self
        if len(self.val) == 2 and not LAZY:
            return Ap(self.val[0], Ap(self.val[1], x))

        if y is not None:
            return B(self.val + [x, y])
        return B(self.val + [x])

    def __repr__(self):
        return "B({0})".format(",".join(map(str, self.val)))


class S(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 2 and not LAZY:
            return Ap(Ap(self.val[0], x), Ap(self.val[1], x))
        return S(self.val + [x])

    def __repr__(self):
        return "S({0})".format(",".join(map(str, self.val)))


class IsNil(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 2 and not LAZY:
            first = self.val[0]()
            assert(isinstance(first, Number))
            if first.val == 0:
                return self.val[1]()
            else:
                return x()
        return IsNil(self.val + [x])

    def __repr__(self):
        return "IsNil({0})".format(",".join(map(str, self.val)))


class Car(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val[0]()
        return Car(self.val + [x])

    def __repr__(self):
        return "Car({0})".format(",".join(map(str, self.val)))


class Cdr(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return x()
        return Cdr(self.val + [x])

    def __repr__(self):
        return "Cdr({0})".format(",".join(map(str, self.val)))


class Add(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val[0]() + x()
        return Add(self.val + [x])

    def __repr__(self):
        return "Add({0})".format(",".join(map(str, self.val)))


class Mul(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val[0]() * x()
        return Mul(self.val + [x])

    def __repr__(self):
        return "Mul({0})".format(",".join(map(str, self.val)))


class Div(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val[0]() // x()
        return Div(self.val + [x])

    def __repr__(self):
        return "Div({0})".format(",".join(map(str, self.val)))


class T(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val[0]()
        return T(self.val + [x])

    def __repr__(self):
        return "T({0})".format(",".join(map(str, self.val)))


class F(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return x()
        return F(self.val + [x])

    def __repr__(self):
        return "F({0})".format(",".join(map(str, self.val)))


class Lt(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            a = self.val[0]()
            while not isinstance(a, Number):
                try:
                    a = a()
                    print(a)
                except:
                    break

            b = x()
            print(a, type(a))
            print(b, type(b))
            assert(isinstance(a, Number))
            assert(isinstance(b, Number))
            if a.val < b.val:
                return T
            else:
                return F
        return Lt(self.val + [x])

    def __repr__(self):
        return "Lt({0})".format(",".join(map(str, self.val)))


class Eq(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            if self.val[0]() == x():
                return T
            else:
                return F
        return Eq(self.val + [x])

    def __repr__(self):
        return "Eq({0})".format(",".join(map(str, self.val)))


class I(object):
    def __init__(self, a=[]):
        self.val = to_list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if not LAZY:
            return x()
        return x

    def __repr__(self):
        return "I({0})".format(",".join(map(str, self.val)))

SH = 0
LIM = 0

class Ap(object):
    def __init__(self, a, b):
        self.first = a
        self.second = b

    def __call__(self):
        if isinstance(self.first, F):
            return I()
        global SH, LIM
        if SH < LIM:
            print(" " * SH, self, ":", self.first, self.second)
        #print("sf:", type(self.first))
        #print("sc:", type(self.second))
        SH += 2
        arg = self.second() if self.second is not None else self.second
        f = self.first
        #print("f:", f)
        #print("type f:", type(f))
        #print("arg:", arg)
        #print("type arg:", type(arg))
        while isinstance(f, Ap):
            f = f()

        try:
            res = f(arg)
        except:
            print("f:", f)
            print("type f:", type(f))
            print("arg:", arg)
            print("type arg:", type(arg))
            arg = arg()
            res = f(arg)

        # if isinstance(res, Ap) and not LAZY: res = res()
        SH -= 2
        if SH < LIM:
            print(" " * SH, "!!! result:", res)
        return res


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
        return Cons, tokens

    try:
        x = int(cur)
        return Number(x), tokens
    except:
        pass

    if cur == "nil":
        return None, tokens

    if cur == "neg":
        return Neg(), tokens

    if cur == "c":
        return C, tokens

    if cur == "b":
        return B, tokens

    if cur == "s":
        return S, tokens

    if cur == "isnil":
        return IsNil, tokens

    if cur == "car":
        return Car, tokens

    if cur == "cdr":
        return Cdr, tokens

    if cur == "eq":
        return Eq, tokens

    if cur == "lt":
        return Lt, tokens

    if cur == "add":
        return Add, tokens

    if cur == "mul":
        return Mul, tokens

    if cur == "div":
        return Div, tokens

    if cur == "i":
        return I, tokens

    if cur == "t":
        return T, tokens

    print("Parse failed on: '{0}'".format(cur))
    assert False

for line in sys.stdin:
    first, last = line.strip().split("=")
    first = first.strip()
    values[first] = parse(last.strip().split(), 0)[0]
    if first == ":1107":
        print(first, values[first]())

print("Parsing {0} entites ok".format(len(values)))

LAZY = False
for v in values:
    break
    print(v, end="...")
    #sys.stderr.write(v)
    sys.stdout.flush()
    print(evaluated(v))

print(evaluated(":20")())
