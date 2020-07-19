import requests
import sys
import itertools
import math
import random
from collections import defaultdict
from common import *

def make_join_request(key):
    m = mod([2, [key, [None, None]]])
    return m

max_shoot_energy = 64

def make_start_request(key, resp):
    # m = mod([3, [key, [None, None]]])
    max_score = flatten(dem(resp))[2][2][0]
    if max_score == 448:
        characteristics = [326, [0, [10, [1, None]]]]
    elif max_score == 512:
        characteristics = [max_score - max_shoot_energy * 4 - 12 * 10 - 2, [max_shoot_energy, [10, [1, None]]]]
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

def make_shoot_request(my_ship, another_ship_pos, power):
    return 2, (my_ship.ship_id, ((another_ship_pos.x, another_ship_pos.y), (power, None)))

def get_gravity(ship_pos):
    gravity = Point(0, 0)
    if abs(ship_pos.x) >= abs(ship_pos.y):
        gravity.x = -signum(ship_pos.x)
    if abs(ship_pos.y) >= abs(ship_pos.x):
        gravity.y = -signum(ship_pos.y)
    return gravity

def calc_real_demage(use_energy, position):
    x = abs(position.x)
    y = abs(position.y)
    if max(x, y) == 0:
        return 0
    ratio = abs(2.0 * min(x, y) / max(x, y) - 1)
    return max(0, int(math.ceil((use_energy * 3 + 1) * ratio - max(x, y))))

all_his_actions = []

def apply_transform(p, xmul, ymul, swap_coords):
    nx = p.x * xmul
    ny = p.y * ymul
    if swap_coords == 1:
        nx, ny = ny, nx
    return Point(nx, ny)

def predict_action(last_action):
    options = defaultdict(lambda: 0)
    options[last_action] = 1
    for i in range(len(all_his_actions) - 1):
        was_action = all_his_actions[i]
        next_action = all_his_actions[i + 1]
        cur_prediction = None
        for xmul in {-1, 1}:
            for ymul in {-1, 1}:
                for swap_coords in {0}:
                    transformed_action = apply_transform(was_action, xmul, ymul, swap_coords)
                    if transformed_action == last_action:
                        cur_prediction = apply_transform(next_action, xmul, ymul, swap_coords)
        if cur_prediction is not None:
            options[cur_prediction] = options[cur_prediction] + 1
    print('predictions: ', options)
    best_prediction = last_action
    best_num = 1
    for k, v in options.items():
        if v > best_num:
            best_prediction = k
            best_num = v
    return best_prediction


def make_commands_request(key, game_state):
    print(game_state.my_type)
    ops = None
    opp_ships = game_state.get_opp_ships()
    if not opp_ships:
        return mod((4, (key, (ops, None))))

    another_ship = opp_ships[0]
    print('his_pos', another_ship.pos)
    his_action = Point(0, 0)
    for his_move in another_ship.prev_moves:
      if his_move.move_type == 0:
        his_action = Point(0, 0) - his_move.pos()
    print('his_action', his_action)
    all_his_actions.append(his_action)
    moves = []
    for dx in range(-1, 2):
      for dy in range(-1, 2):
        moves.append(Point(dx, dy))
    can_skip_accelerate = False
    for ship in game_state.ships:
      if ship.player_type == game_state.my_type:
        print("ship coords =", ship.pos.aslist())
        print('my speed', ship.speed.aslist())
        best_distance = (787788789, -1)
        best_sequence = []
        for reps in range(2, 4):
          for sequence in itertools.product(moves, repeat = reps):
            my_pos = Point(ship.pos.x, ship.pos.y)
            his_pos = Point(another_ship.pos.x, another_ship.pos.y)
            my_speed = Point(ship.speed.x, ship.speed.y)
            his_speed = Point(another_ship.speed.x, another_ship.speed.y)
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
            if cmin[0] < 787 and sequence[0] == Point(0, 0):
                can_skip_accelerate = True
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
        # TODO: change random?
        if can_skip_accelerate and (ship.tiredness > 10 or (random.randint(0, 4) != 0 and game_state.my_type == ATTACKER_ID)):
            dx = 0
            dy = 0
            print("skip accelerate at this point, because too tired", ship.tiredness)
        print("go", dx, dy)
        ops = ((0, (ship.ship_id, ((dx, dy), None))), ops)

        if best_distance[1] == 0 and best_distance[2] <= 1 and game_state.my_type == 0 and len(opp_ships) == 1:
          print("explode!")
          ops = ((1, (ship.ship_id, None)), ops)

        if game_state.my_type == ATTACKER_ID:
            best_shot = (-1, None)
            for another_ship in game_state.ships:
                if another_ship.player_type == game_state.my_type:
                    continue
                his_pos = Point(another_ship.pos.x, another_ship.pos.y)
                his_speed = Point(another_ship.speed.x, another_ship.speed.y)
                prediction = predict_action(his_action)
                if another_ship.energy == 0:
                    prediction = Point(0, 0)
                his_speed += prediction
                his_speed += get_gravity(his_pos)
                his_pos += his_speed

                my_pos = Point(ship.pos.x, ship.pos.y)
                my_speed = Point(ship.speed.x, ship.speed.y)
                my_speed += Point(-dx, -dy) # very bad '-' :(
                my_speed += get_gravity(my_pos)
                my_pos += my_speed

                diff_to_him = his_pos - my_pos
                use_demage = min(max_shoot_energy, ship.tiredness_limit - ship.tiredness) # TODO: change it!
                real_demage = calc_real_demage(use_demage, diff_to_him)
                if real_demage > use_demage * 1.7 and use_demage > max_shoot_energy - 10 and real_demage > best_shot[0]: # TODO: change condition!
                    best_shot = (real_demage, make_shoot_request(ship, his_pos, use_demage))
                    print('shoot?, use {}, expected demage {}'.format(use_demage, real_demage))
            if best_shot[0] != -1:
                print("shoot!", best_shot[0])
                ops = (best_shot[1], ops)

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
