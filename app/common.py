from itertools import starmap
import requests

local_url = "https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=1242ae59bc9f4385b3c3eaa60764a09c"

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
    if x is None:
        return "00"
    if isinstance(x, int) or isinstance(x, str):
        return mod_num(int(x))
    if isinstance(x, list) or isinstance(x, tuple):
        assert(len(x) == 2)
        return "11" + mod(x[0]) + mod(x[1])

    print(x, type(x))
    fail


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


def demrec(s):
    assert len(s) >= 2
    if s[:2] == "01":
        x, s = parse_int(s[2:])
        return x, s

    if s[:2] == "10":
        x, s = parse_int(s[2:])
        return -x, s

    if s[:2] == "11":
        s = s[2:]
        x, s = demrec(s)
        y, s = demrec(s)
        return (x, y), s

    if s[:2] == "00":
        return None, s[2:]

    assert False


def dem(s):
    return demrec(s)[0]

def send_request(x, url):
    res = requests.post(url, data=x)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('_response body:', res.text)
        exit(2)
    # print('Server response:', res.text)
    return res.text

class Point(object):
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], list) or isinstance(args[0], tuple):
                self.x = args[0][0]
                self.y = args[0][1]
            else:
                self.x = args[0].x
                self.y = args[0].y
        else:
            assert(len(args) == 2)
            self.x = args[0]
            self.y = args[1]

    def aslist(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Move(object):
    def __init__(self, move_type, arg):
        self.move_type = move_type
        self.arg = arg


class Ship(object):
    def __init__(self, pos, speed, player_type, ship_id, skills, prev_moves):
        self.pos = pos
        self.speed = speed
        self.player_type = player_type
        self.ship_id = ship_id
        self.skills = list(skills)
        self.prev_moves = list(prev_moves)


def parse_ship(ship_list):
    ship_info = ship_list[0]
    pos = Point(ship_info[2])
    speed = Point(ship_info[3])
    player_type = ship_info[0]
    ship_id = ship_info[1]
    skills = ship_info[4]

    prev_moves = [] if ship_list[1] is None else list(starmap(Move, ship_list[1]))

    return Ship(pos, speed, player_type, ship_id, skills, prev_moves)


class GameState(object):
    def __init__(self, a):
        self.ships = []
        self.my_type = -1
        self.game_finished = False
        self.world_size = -1
        self.planet_size = -1

        try:
            if a[0] == 0:
                self.game_finished = True
            else:
                self.ships = list(map(parse_ship, a[3][2]))
                self.my_type = a[2][1]
                self.world_size = a[2][3][1]
                self.planet_size = a[2][3][0] # not sure?
        except Exception as e:
            print("Can not parse game state:", e, a)
            pass


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

#resp = flatten((1, (1, ((256, (1, ((448, (1, (64, None))), ((16, (128, None)), (None, None))))), ((2, ((16, (128, None)), ((((1, (0, ((-30, 48), ((-2, 0), ((110, (64, (4, (16, None)))), (8, (64, (1, None)))))))), (((0, ((1, -1), None)), None), None)), (((0, (1, ((27, -48), ((0, 0), ((324, (0, (10, (1, None)))), (0, (64, (2, None)))))))), (((0, ((0, 1), None)), None), None)), None)), None))), None)))))
#resp = [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [2, [16, 128], [[[1, 0, [45, -41], [-2, 0], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-45, 41], [2, 0], [112, 64, 4, 16], 0, 64, 1], None]]]]
#print(GameState(resp).ships[1].pos.y)

"""
turn 3/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [2, [16, 128], [[[1, 0, [45, -41], [-2, 0], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-45, 41], [2, 0], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 4/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [3, [16, 128], [[[1, 0, [42, -41], [-3, 0], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-42, 41], [3, 0], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 5/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [4, [16, 128], [[[1, 0, [38, -41], [-4, 0], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-38, 41], [4, 0], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 6/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [5, [16, 128], [[[1, 0, [34, -40], [-4, 1], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-34, 40], [4, -1], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 7/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [6, [16, 128], [[[1, 0, [30, -38], [-4, 2], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-30, 38], [4, -2], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 8/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [7, [16, 128], [[[1, 0, [26, -35], [-4, 3], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-26, 35], [4, -3], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 9/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [8, [16, 128], [[[1, 0, [22, -31], [-4, 4], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-22, 31], [4, -4], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 10/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [9, [16, 128], [[[1, 0, [18, -26], [-4, 5], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-18, 26], [4, -5], [112, 64, 4, 16], 0, 64, 1], None]]]]
====================
turn 11/2262
sent -> [4, 289682608305907367, None]
got  <- [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]], [10, [16, 128], [[[1, 0, [14, -20], [-4, 6], [1, 2, 3, 4], 0, 64, 1], None], [[0, 1, [-14, 20], [4, -6], [112, 64, 4, 16], 0, 64, 1], None]]]]
"""
