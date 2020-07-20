# icfpc2020

TODO: write more 

# Utils

## Galaxy evaluator
```
cd play
g++ -std=c++11 -o sol sol.cpp
python3 x.py
```
TODO: write description

## Strategy
```
python3 app/main.py
```

## Visualizers/Tools

* app/play-non-rated.py &mdash; use API to create testing games with top players from scoreboard
* app/logviewer.py &mdash; reads strategy log (which contains all interactions with server) from stdin, and vizualize
  * Use keys `o`, `p` to switch between moves
  * Use keys `1`, `2` to zoom
* app/localrunner.py &mdash; creates a multiplayer game, runs two local bot instances with correct keys, pipe bots logs to logviewer to get a vizualization

# Galaxy investigation

TODO: write more
* 64 -> 128 for tiredness limit
* 1 -> 2 for moves limit
* detonation demage calculation
* shoot demage calculation

# Strategy ideas
## Defender
TODO: write more

## Attacker
TODO: write about chosed skills configuration
* Shoot only at good positions (see shoot demage calculation).
* Shoot only if demage is big enough to decrease target's energy (if you only increase tiredness, and it doesn't reach tiredness limit, it will probably recover in a several turns).
* Try not to spend energy for acceleration if it is not really needed (because of that we can choose skill configuration with bigger max_demage parameter).
* If you decide to shoot on current move, you can change your acceleration to get to a position with much better demage (see strange shoot demage calculation).
* It is very important to guess where the target will be after the next move. If you don't guess, demage will be 4 or 16 times less than expected, and it probably will only change tiredness, which will be recovered soon.
* To guess next target's acceleration change, we look at his last move, and try to predict next move based on history of all previous moves. We find all previous moves, which are the same as last move, and look what were the next move for them. Also, as we don't have a long history, we try to use moves, which could be received from last move by reflection over coordinate axes.
* Common strategy for defenders &mdash; split spaceship into several components. To prevent this we need to shoot at ships with big health if we can.
* If target has 0 energy &mdash; it is very easy to predict where it will be after next move.

