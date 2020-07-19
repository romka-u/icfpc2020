import requests
import sys
from common import *

def make_join_request(key):
    m = mod([2, [key, [None, None]]])
    return m

def make_start_request(key, resp):
    # m = mod([3, [key, [None, None]]])
    m = mod([3, [key, [[326, [0, [10, [1, None]]]], None]]])
    return m

def signum(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0

def make_commands_request(key, game_state):
    print(game_state.my_type)
    ops = None
    for ship in game_state.ships:
      if ship.player_type == game_state.my_type:
        print("ship coords =", ship.pos.aslist())
        dx = -signum(ship.pos.x)
        dy = -signum(ship.pos.y)
        if signum(ship.speed.x) == signum(ship.pos.x):
          dx = 0
        if signum(ship.speed.y) == signum(ship.pos.y):
          dy = 0
        print("go", dx, dy)
        ops = ((0, (ship.ship_id, ((dx, dy), None))), ops)
    m = mod((4, (key, (ops, None))))
    return m

def send(x):
    url = sys.argv[1] + "/aliens/send"
    if sys.argv[1] == "local":
        url = local_url
    return send_request(x, url)

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    join_request = make_join_request(player_key)
    print("->", dem(join_request))
    game_response = send(join_request)
    print("<-", dem(game_response))

    start_request = make_start_request(player_key, game_response)
    print("->", dem(start_request))
    game_response = send(start_request)
    print("<-", dem(game_response))
    sys.stdout.flush()

    while True:
        game_state = GameState(flatten(dem(game_response)))
        if game_state.game_finished:
            break
        commands_request = make_commands_request(player_key, game_state)
        print("->", dem(commands_request))
        game_response = send(commands_request)
        print("<-", dem(game_response))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
