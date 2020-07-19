import requests
import sys
from common import *

def make_join_request(key):
    m = mod([2, [key, [None, None]]])
    return m

def make_start_request(key, resp):
    # m = mod([3, [key, [None, None]]])
    max_score = flatten(dem(resp))[2][2][0]
    if max_score == 448:
        characteristics = [326, [0, [10, [1, None]]]]
    elif max_score == 512:
        characteristics = [326, [16, [10, [1, None]]]]
    else:
        #TODO: FIX IT PLEASE!
        characteristics = [1, [1, [1, [1, None]]]]
    m = mod([3, [key, [characteristics, None]]])
    return m

def signum(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0

def make_shoot_request(my_ship, another_ship, power):
    return 2, (my_ship.ship_id, ((another_ship.pos.x, another_ship.pos.y), (power, None)))

def make_commands_request(key, game_state):
    print(game_state.my_type)
    ops = None
    another_ship = None
    for ship in game_state.ships:
        if ship.player_type != game_state.my_type:
            another_ship = ship
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
        # uncomment, when you think it is useful
        # if game_state.my_type == ATTACKER_ID and another_ship is not None:
        #     ops = (make_shoot_request(ship, another_ship, 1), ops)
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
