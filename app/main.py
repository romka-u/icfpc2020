import requests
import sys

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


def make_join_request(key):
    m = mod([2, [key, [None, None]]])
    return m

def make_start_request(key, resp):
    # m = mod([3, [key, [None, None]]])
    m = mod([3, [key, [[112, [64, [4, [16, None]]]], None]]])
    return m

def signum(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0

def make_commands_request(key, resp):
    my_coords = resp[1][1][1][0][1][1][0][0][0][1][1][0]
    print("my_coords =", my_coords)
    dx = signum(my_coords[0])
    dy = signum(my_coords[1])
    print("go", dx, dy)
    m = mod((4, (key, (((0, (0, ((dx, dy), None))), None), None))))
    #m = mod((4, (key, (None, None))))
    return m

def send(x):
    url = sys.argv[1] + "/aliens/send"
    if sys.argv[1] == "local":
        url = "https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=1242ae59bc9f4385b3c3eaa60764a09c"
    res = requests.post(url, data=x)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('_response body:', res.text)
        exit(2)
    # print('Server response:', res.text)
    return res.text

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    join_request = make_join_request(player_key)
    print("->", dem(join_request))
    game_response = send(join_request)
    print("<-", dem(game_response))
    my_type = game_response[1][1][0][1][0]
    print("my_type =", my_type)

    start_request = make_start_request(player_key, game_response)
    print("->", dem(start_request))
    game_response = send(start_request)
    print("<-", dem(game_response))
    sys.stdout.flush()

    while True:
        commands_request = make_commands_request(player_key, game_response)
        print("->", dem(commands_request))
        game_response = send(commands_request)
        print("<-", dem(game_response))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
