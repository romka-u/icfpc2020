import requests
import sys
import itertools
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

def get_gravity(ship_pos):
    gravity = Point(0, 0)
    if abs(ship_pos.x) >= abs(ship_pos.y):
        gravity.x = -signum(ship_pos.x)
    if abs(ship_pos.y) >= abs(ship_pos.x):
        gravity.y = -signum(ship_pos.y)
    return gravity

def make_commands_request(key, game_state):
    print(game_state.my_type)
    ops = None
    opp_ships = game_state.get_opp_ships()
    if not opp_ships:
        return mod((4, (key, (ops, None))))

    another_ship = opp_ships[0]
    print('his_pos', another_ship.pos)
    his_action = Point(0, 0) - another_ship.get_last_move()
    print('his_action', his_action)
    moves = [Point(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]

    for ship in game_state.ships:
      if ship.player_type == game_state.my_type:
        print("ship coords =", ship.pos.aslist())
        print('my speed', ship.speed.aslist())
        best_distance = (787788789, -1)
        best_sequence = []
        for reps in range(2, 4):
          for sequence in itertools.product(moves, repeat=reps):
            my_pos = ship.pos.clone()
            his_pos = another_ship.pos.clone()
            my_speed = ship.speed.clone()
            his_speed = another_ship.speed.clone()
            cmin = (787788, None, None)
            for i in range(30):
              if i < len(sequence):
                my_speed += sequence[i]
              my_speed += get_gravity(my_pos)
              my_pos += my_speed
              his_speed += his_action
              his_speed += get_gravity(his_pos)
              his_pos += his_speed
              dist = abs(my_pos.x - his_pos.x) + abs(my_pos.y - his_pos.y)
              mmdist = max(abs(my_pos.x - his_pos.x), abs(my_pos.y - his_pos.y))
              #if i < 10:
              #  print('iter', sequence, i, my_pos.aslist(), my_speed.aslist(), his_pos.aslist(), his_speed.aslist())
              if dist < cmin[0]:
                cmin = (dist, i, mmdist)
              if max(abs(my_pos.x), abs(my_pos.y)) <= game_state.planet_size:
                cmin = (1000 if game_state.my_type == 0 else -1000, -i, 1e9)
                break
              if max(abs(my_pos.x), abs(my_pos.y)) > game_state.world_size:
                cmin = (1000 if game_state.my_type == 0 else -1000, -i, 1e9)
                break
              #if max(abs(his_pos.x), abs(his_pos.y)) <= 16: # !! change to real constant
              #  break
            if game_state.my_type == 1:
              cmin = (-cmin[0], cmin[1], cmin[2])
            if cmin < best_distance:
              best_distance = cmin
              best_sequence = sequence
          if best_distance[0] != 1000:
            break
          #print(sequence)
          #print(min_dist)
        #print('-- --')
        print('dist', best_distance)
        print(best_sequence)

        dx = -best_sequence[0].x
        dy = -best_sequence[0].y
        print("go", dx, dy)
        ops = ((0, (ship.ship_id, ((dx, dy), None))), ops)

        if best_distance[1] == 0 and best_distance[2] <= 1 and game_state.my_type == 0 and len(opp_ships) == 1:
          print("explode!")
          ops = ((1, (ship.ship_id, None)), ops)

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
