# icfpc2020

We are RGBTeam, and this is our ICFPC 2020 repository.

Team members:
* Roman Udovichenko
* Gennady Korotkevich
* Borys Minaiev

No points for guessing the origins of our team name :)

We snatched the first place in the rounds 2-7 leaderboard (https://icfpcontest2020.github.io/#/scoreboard#full),
and we hope our strategy will also perform well in the final round!

# Utils

## Galaxy evaluator
```
cd play
g++ -std=c++11 -o sol sol.cpp
python3 x.py
```

Use keys `1` and `2` for zoom and mouse for clicking on elements.

<img src="https://sun6-16.userapi.com/8UCLr5bheXd7BkEesCzo54Gpk-emFPL7ZStxmw/GpQ0cSOPWPY.jpg" width="600">

### Galaxy evaluator description
Expressions are stored as trees of nodes: 
```
struct Node {
  string text;
  Node* left;
  Node* right;
};
```
Nodes with `text == "ap"` have two children, other nodes have none.

A node can be present in different expressions and thus have multiple parents.
This design helps to reuse calculations for similar subtrees that appear e.g. as a result of applying the S combinator.

Node's `eval` method forces its evaluation, which proceeds as follows: 
* If it is not an `ap` node, stop.
* Otherwise:
  * call `eval` for its left subtree;
  * locate the leftmost non-`ap` node;
  * if the number of `ap`s above it matches the number of its arguments, apply the function in-place and start all over, otherwise stop.

Note that list (`cons`) elements may not be evaluated by calling `eval` on the list.
Continuosly applying `car` and `cdr` to the list forces element evaluation.

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


<img src="https://sun6-14.userapi.com/8zJHgHRQc6G8WbsmbNSckDNAkzVv-1A9mvzoMA/fRqXZ30GKkg.jpg" width="600">

# Galaxy investigation

Note that in this document "temperature" is called "tiredness", and "critical temperature" is called "tiredness limit" :)

It took us a lot of time (and pretty much one person's sleepless night) to find out how other teams managed increase their tiredness limit to 128 while the standard one was 64.

The JOIN request specification suggested that the last argument is an "unknown list".
Experiments showed that this list can only accepts integers and not other lists (otherwise the request failed).

It turned out that the boot screen contained several clickable "easter eggs":
* a Memory-like game. After winning it, your tiredness limit in multiplayer games increases to 128. This is implemented via sending a particular "magic number" in the JOIN request. 
* an unwinnable 3x3 tic-tac-toe game, with an AI playing against you, and the goal of getting all 12 possible drawn final game states. After doing that, your "thrust per turn" limit increases from 1 to 2. This is implemented in the same way, with a different "magic number".
* a diagram showing the amount of damage dealt by shooting. In particular, shot damage is maximized is its direction is a multiple of 45 degrees. We experimented a lot with shot damage before we found this diagram, and found a formula that allowed to approximate shot damage very well, missing just by 1 sometimes:
  * Assuming you shoot in the `(x, y)` direction: 
  * `ratio = abs(2.0 * min(x, y) / max(x, y) - 1)`
  * `damage = max(0, ceil((power * 3 + 1) * ratio - max(x, y))))`
* a diagram showing the amount of damage dealt to the ships via detonation. We couldn't figure out the exact meaning of this diagram, so we tried to approximate it, but didn't spend too much time on it.

# Strategy ideas
## Initial skills configuration
We used skills `(152, 0, 8, 100)` for defender and `(134, 64, 10, 1)` for attacker. The main idea was to make first parameter as small as possible, but still big enough to fly during whole round. Third parameter should be at least 8 to accelerate without making damage to itself. All left skills were used for 4-th parameter in case of defender and for 2-nd parameter in case of attacker.

## Defender
* Initial ideas for finding the direction to thrust: 
  * Brute force over the next 2-3 thrust directions.
  * Choose the sequence of thrust directions that allows you to stay as far as possible from the attacking ships (assuming they don't thrust) in the following 30 time units.
  * Apply thrust equal to the first element of this "best" sequence.
* Later it became clear that spawning small ships is required, so we changed our strategy:
  * Only one "mothership" is controlled. 
  * If the mothership's current speed allows it to "orbit" until the end of the game, spawn a microship with 0 energy (unless we did the same on the last time unit, in which case proceed to the next step &mdash; it doesn't make sense to spawn several ships at the same place).
  * Otherwise, brute force the next several thrust directions.
  * Find the shortest sequence that allows the mothership to "orbit" afterwards.
  * Apply thrust equal to the first element of this sequence.
  * Note that attacking ship positions are totally disregarded in this strategy &mdash; we just hope to spawn enough small ships to survive until the end of the game.

## Attacker
* Shoot only at good positions (see shot damage calculation).
* Shoot only if damage is big enough to decrease target's energy (if you only increase tiredness, and it doesn't reach tiredness limit, it will probably recover in a several turns).
* Try not to spend energy for acceleration if it is not really needed (because of that we can choose skill configuration with bigger max_damage parameter).
* If you decide to shoot on current move, you can change your acceleration to get to a position with much better damage (see strange shoot damage calculation).
* It is very important to guess where the target will be after the next move. If you don't guess, damage will be 4 or 16 times less than expected, and it probably will only change tiredness, which will be recovered soon.
* To guess next target's acceleration change, we look at his last move, and try to predict next move based on history of all previous moves. We find all previous moves, which are the same as last move, and look what were the next move for them. Also, as we don't have a long history, we try to use moves, which could be received from last move by reflection over coordinate axes.
* Common strategy for defenders &mdash; split spaceship into several components. To prevent this we need to shoot at ships with big health if we can.
* If target has 0 energy &mdash; it is very easy to predict where it will be after next move.

