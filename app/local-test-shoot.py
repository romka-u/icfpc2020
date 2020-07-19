from common import *
import subprocess

def create_new_game_request():
    m = mod([1, [0, None]])
    return m

def create_join_local_game_request(key):
    m = mod([5, [key, None]])
    return m

def send(x):
    print("->", dem(x))
    response = flatten(dem(send_request(x, local_url)))
    print("<-", response)
    return response

val = {}

def run_one(shift):
    print('start new game')
    create_game_response = send(create_new_game_request())
    attacker_key = str(create_game_response[1][0][1])
    defender_key = str(create_game_response[1][1][1])
    # or i mixed up them?
    print("attacker_key:", attacker_key)
    print("defender_key:", defender_key)

    # ignore this response?
    join_local_response = send(create_join_local_game_request(attacker_key))

    print('run attack process')
    attacker_log = 'tmp/attacker.log'
    with open(attacker_log, 'wb') as out:
        attacker_process = subprocess.Popen(['python3', 'main-test-shoot.py', 'local', attacker_key, str(shift)], stdout=out)

    print('run defender process')
    with open('tmp/defender.log', 'wb') as out:
        defender_process = subprocess.Popen(['python3', 'main.py', 'local', defender_key], stdout=out)

    # viewer_cmd = 'python3 logviewer.py < ' + attacker_log
    # viewer_process = subprocess.Popen(viewer_cmd, shell=True)
    # viewer_process.wait()
    # print('viewer is closed, killing players')
    attacker_process.wait()
    defender_process.wait()
    print('game for shift {} is finished'.format(shift))

    global val
    cnt = 0
    with open("log.txt", "r") as flog:
        for line in flog:
            a = list(map(int, line.split()))
            if a[0] == shift:
                val[(a[0], a[1])] = a[2]
                cnt += 1
    print('got {0} values'.format(cnt))

def main():
    for shift in range(0, 30):
        run_one(shift)

    global val
    for shift in range(0, 30):
        print(" ".join(str(val[(shift, y)]) if (shift, y) in val else "?" for y in range(0, 30)))

if __name__ == '__main__':
    main()
