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
        characteristics = [300, [20, [10, [1, None]]]]
    elif max_score == 512:
        characteristics = [300, [20, [10, [1, None]]]]
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

def make_shoot_request(my_ship, x, y, power):
    return 2, (my_ship.ship_id, ((x, y), (power, None)))

move_id = -1

def make_commands_request(key, game_state):
    global move_id
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
        if abs(ship.pos.x) > abs(ship.pos.y):
            dy = 0
        if abs(ship.pos.y) > abs(ship.pos.x):
            dx = 0
        print("go", dx, dy)
        ops = ((0, (ship.ship_id, ((dx, dy), None))), ops)
        # uncomment, when you think it is useful
        if game_state.my_type == ATTACKER_ID and ship.tiredness_limit - ship.tiredness >= 20:
            move_id = move_id + 1
            shoot_dx = int(sys.argv[3]) # -move_id #move_id // N - N // 2
            shoot_dy = move_id #move_id % N - N // 2
            print('shoot: ', shoot_dx, shoot_dy)
            ops = (make_shoot_request(ship, ship.pos.x + shoot_dx, ship.pos.y + shoot_dy, 20), ops)
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

    ft = open("log.txt", "w")

    while True:
        game_state = GameState(flatten(dem(game_response)))
        if game_state.game_finished:
            break
        commands_request = make_commands_request(player_key, game_state)
        print("->", dem(commands_request))
        game_response = send(commands_request)
        gr = GameState(flatten(dem(game_response)))
        for sh in gr.ships:
            if sh.player_type == gr.my_type:
                flag = False
                for m in sh.prev_moves:
                    if m.move_type == 0:
                        flag = True

                for m in sh.prev_moves:
                    if m.move_type == 2:
                        delta = m.pos() - sh.pos
                        ft.write("{} {} {}\n".format(delta.x, delta.y, m.args[2]))
                        ft.flush()
        print("<-", dem(game_response))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
