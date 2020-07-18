import sys

sys.setrecursionlimit(1234567)
values = {}
cache = {}

def evaluated(sym):
    # print(sym, end="...")
    # sys.stdout.flush()
    if sym not in cache:
        cache[sym] = values[sym]()
    return cache[sym]


def to_list(a):
    global LAZY
    while isinstance(a, Ap):
        a = a()
    try:
        return list(a)
    except:
        return [a]


class Symbol(object):
    def __init__(self, key):
        self.key = key

    def __call__(self, x=None):
        if x is None:
            return evaluated(self.key)
        return Ap(values[self.key], x)()

    def __repr__(self):
        return self.key


class Cons(object):
    def __init__(self, val=[]):
        self.val = to_list(val)

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
        self.val = val

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(Ap(self.val[0], x), self.val[1])()
        return C(self.val + [x])

    def __repr__(self):
        return "C({0})".format(",".join(map(str, self.val)))


class B(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(self.val[0], Ap(self.val[1], x))()

        return B(self.val + [x])

    def __repr__(self):
        return "B({0})".format(",".join(map(str, self.val)))


class S(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 2:
            return Ap(Ap(self.val[0], x), Ap(self.val[1], x))()
        return S(self.val + [x])

    def __repr__(self):
        return "S({0})".format(",".join(map(str, self.val)))


class IsNil(object):
    def __call__(self, x):
        if isinstance(x() if isinstance(x, Ap) else x, Nil):
            return T()
        else:
            return F()

    def __repr__(self):
        return "IsNil"


class Car(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]()
        if isinstance(x, Ap):
            x = x()
        if not isinstance(x, Cons):
            print(x)
            print(type(x))
        assert isinstance(x, Cons)
        self.val += x.val
        # if len(self.val) == 2:
        return self.val[0]()

        return Car(self.val + [x])

    def __repr__(self):
        return "Car({0})".format(",".join(map(str, self.val)))


class Cdr(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return x()
        if isinstance(x, Ap):
            x = x()
        if not isinstance(x, Cons):
            print(x)
            print(type(x))
        assert isinstance(x, Cons)
        self.val += x.val
        # if len(self.val) == 2:
        return self.val[1]()
        return Cdr(self.val + [x])

    def __repr__(self):
        return "Cdr({0})".format(",".join(map(str, self.val)))


class Add(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() + x()
        return Add(self.val + [x])

    def __repr__(self):
        return "Add({0})".format(",".join(map(str, self.val)))


class Mul(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() * x()
        return Mul(self.val + [x])

    def __repr__(self):
        return "Mul({0})".format(",".join(map(str, self.val)))


class Div(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]() // x()
        return Div(self.val + [x])

    def __repr__(self):
        return "Div({0})".format(",".join(map(str, self.val)))


class T(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return self.val[0]()
        return T(self.val + [x])

    def __repr__(self):
        return "T({0})".format(",".join(map(str, self.val)))


class F(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            return x()
        return F(self.val + [x])

    def __repr__(self):
        return "F({0})".format(",".join(map(str, self.val)))


class Lt(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        if len(self.val) == 1:
            a = self.val[0]()
            b = x()
            #print(a, type(a))
            #print(b, type(b))
            assert(isinstance(a, Number))
            assert(isinstance(b, Number))
            if a.val < b.val:
                return T()
            else:
                return F()
        return Lt(self.val + [x])

    def __repr__(self):
        return "Lt({0})".format(",".join(map(str, self.val)))


class Eq(object):
    def __init__(self, val=[]):
        self.val = val

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
        return "Eq({0})".format(",".join(map(str, self.val)))


class I(object):
    def __init__(self, val=[]):
        self.val = val

    def __call__(self, x):
        return x

    def __repr__(self):
        return "I({0})".format(",".join(map(str, self.val)))


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

    def __call__(self):
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
    print(v, end="...")
    #sys.stderr.write(v)
    sys.stdout.flush()
    print(evaluated(v))

