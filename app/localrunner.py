from common import *
import subprocess

def create_new_game_request():
    m = mod([1, [0, None]])
    return m

def cretea_join_local_game_request(key):
    m = mod([5, [key, None]])
    return m

def send(x):
    print("->", dem(x))
    response = flatten(dem(send_request(x, local_url)))
    print("<-", response)
    return response

def main():
    print('start new game')
    create_game_response = send(create_new_game_request())
    attacker_key = str(create_game_response[1][0][1])
    defender_key = str(create_game_response[1][1][1])
    # or i mixed up them?
    print("attacker_key:", attacker_key)
    print("defender_key:", defender_key)

    # ignore this response?
    join_local_response = send(cretea_join_local_game_request(attacker_key))

    print('run attack process')
    with open('tmp/attacker.log', 'wb') as out:
        attacker_process = subprocess.Popen(['python3', 'main.py', 'local', attacker_key], stdout=out)

    print('run defender process')
    with open('tmp/defender.log', 'wb') as out:
        defender_process = subprocess.Popen(['python3', 'main.py', 'local', defender_key], stdout=out)

    print('waiting till end, logs are inside tmp/')
    attacker_process.wait()
    defender_process.wait()
    print('game is finished')


if __name__ == '__main__':
    main()
