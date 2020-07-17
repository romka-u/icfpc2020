import sys

sys.setrecursionlimit(123456)
values = {}
cache = {}
LAZY = True

def evaluated(sym):
    if sym not in cache:
        cache[sym] = values[sym]()
    return cache[sym]


class Symbol(object):
    def __init__(self, val):
        self.val = val

    def __call__(self, x=None):
        if LAZY:
            if x is None:
                return self
            return Symbol("{0}({1})".format(self.val, x))

        if x is None:
            return evaluated(self.val)
        return evaluated(self.val)(x)

    def __repr__(self):
        return self.val


class Cons(object):
    def __init__(self, a=[]):
        self.val = list(a)

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
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return C(self.val + [x])

    def __repr__(self):
        return "C({0})".format(",".join(map(str, self.val)))


class B(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return B(self.val + [x])

    def __repr__(self):
        return "B({0})".format(",".join(map(str, self.val)))


class S(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return S(self.val + [x])

    def __repr__(self):
        return "S({0})".format(",".join(map(str, self.val)))


class IsNil(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return IsNil(self.val + [x])

    def __repr__(self):
        return "IsNil({0})".format(",".join(map(str, self.val)))


class Car(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return Car(self.val + [x])

    def __repr__(self):
        return "Car({0})".format(",".join(map(str, self.val)))


class Cdr(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return Cdr(self.val + [x])

    def __repr__(self):
        return "Cdr({0})".format(",".join(map(str, self.val)))


class Add(object):
    def __init__(self, a=[]):
        self.val = list(a)

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
        self.val = list(a)

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
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        if len(self.val) == 1 and not LAZY:
            return self.val() / x()
        return Div(self.val + [x])

    def __repr__(self):
        return "Div({0})".format(",".join(map(str, self.val)))


class Lt(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return Lt(self.val + [x])

    def __repr__(self):
        return "Lt({0})".format(",".join(map(str, self.val)))


class Eq(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return Eq(self.val + [x])

    def __repr__(self):
        return "Eq({0})".format(",".join(map(str, self.val)))


class T(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return T(self.val + [x])

    def __repr__(self):
        return "T({0})".format(",".join(map(str, self.val)))


class I(object):
    def __init__(self, a=[]):
        self.val = list(a)

    def __call__(self, x=None):
        if x is None:
            return self
        return x

    def __repr__(self):
        return "I({0})".format(",".join(map(str, self.val)))


class Ap(object):
    def __init__(self, a, b):
        self.first = a
        self.second = b

    def __call__(self):
        # print(self, ":", self.first, self.second)
        return self.first()(self.second() if self.second is not None else self.second)


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

    def __div__(self, other):
        return Number(self.val / other.val)

    def __neg__(self):
        return Number(-self.val)


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
        return Neg, tokens

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

    print(cur)
    assert False

for line in sys.stdin:
    first, last = line.strip().split("=")
    first = first.strip()
    values[first] = parse(last.strip().split(), 0)[0]
    if first == ":1202":
        print(first, values[first]())

print("Parsing {0} entites ok".format(len(values)))

LAZY = False
for v in values:
    break
    # if v <= ":1096":
    print(v, end="...")
    sys.stdout.flush()
    print(values[v]())
