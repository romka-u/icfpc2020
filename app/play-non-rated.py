import requests
import argparse
import sys
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tournament", required=True)
    parser.add_argument("-a", "--attack", action="store_true")
    parser.add_argument("-d", "--defend", action="store_true")
    return parser.parse_args()

def get_submissions(t):
    url = "https://icfpc2020-api.testkontur.ru/scoreboard/{}?apiKey=1242ae59bc9f4385b3c3eaa60764a09c".format(t)
    r = requests.get(url)
    js = r.json()
    res = []
    for rec in js["teams"]:
        res.append((rec["rating"]["mu"], rec["team"]["teamName"], rec["submission"]["submissionId"]))
    res.sort(key=lambda x: -x[0])
    return res

def get_my_last_submission():
    url = "https://icfpc2020-api.testkontur.ru/submissions?apiKey=1242ae59bc9f4385b3c3eaa60764a09c"
    r = requests.get(url)
    js = r.json()
    return (js[0]["submissionId"], js[0]["commitMessage"])

def create_game(attacker, defender):
    url = "https://icfpc2020-api.testkontur.ru/games/non-rating/run?attackerSubmissionId={}&defenderSubmissionId={}&apiKey=1242ae59bc9f4385b3c3eaa60764a09c".format(attacker, defender)
    while True:
        r = requests.post(url)
        js = r.json()
        try:
            print("Created game", js["gameId"])
            break
        except:
            print("Failed to create game:", js, "- waiting 2 secs...")
            time.sleep(2)

def main():
    args = parse_args()
    submissions = get_submissions(args.tournament)
    for i, s in enumerate(submissions[:20]):
        print("{0:2d} {1:5.2f} {2} {3}".format(i, s[0], s[1], s[2]))
    print("=" * 30)
    my_sub = get_my_last_submission()
    print("My last submission: {0} ({1})".format(*my_sub))
    print("Enter ids of teams to play, separated by space:", end=" ")
    sys.stdout.flush()
    try:
        ids = list(map(int, sys.stdin.readline().split()))
    except Exception as e:
        print("Failed to parse team ids:", e)

    print("Enter number of games with every team:", end=" ")
    sys.stdout.flush()
    n = int(sys.stdin.readline().strip())

    for id in ids:
        for i in range(n):
            if args.attack:
                create_game(my_sub[0], submissions[id][2])
            if args.defend:
                create_game(submissions[id][2], my_sub[0])


if __name__ == "__main__":
    main()
