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

def make_join_request(key):
    m = mod([2, [key, None]])
    return m

def make_start_request(key, resp):
    m = mod([3, [key, [[5, [0, [0, [0, None]]]], None]]])
    return m

def make_commands_request(key, resp):
    m = mod((4, (key, (None, None))))
    return m

def send(x):
    res = requests.post(sys.argv[1], data=x)
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
    print("jr:", join_request)
    game_response = send(join_request)
    print("game_response:", game_response)

    start_request = make_start_request(player_key, game_response)
    print("sr:", start_request)
    game_response = send(start_request)
    print("game_response:", game_response)

    while True:
        commands_request = make_commands_request(player_key, game_response)
        # print("cr:", commands_request)
        game_response = send(commands_request)
        # print("game_response:", game_response)


if __name__ == '__main__':
    main()
