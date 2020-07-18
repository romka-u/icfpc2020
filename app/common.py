from itertools import starmap

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

        try:
            self.ships = list(map(parse_ship, a[3][2]))
            self.my_type = a[2][1]
        except Exception as e:
            print("Can not parse game state:", e)
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
