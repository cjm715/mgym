# Multi-agent gym environments


This repository has a collection of multi-agent [OpenAI gym](https://github.com/openai/gym) environments.

DISCLAIMER: This project is in its early stages --- it is still a work in progress.


## Dependencies
* `gym`
* `numpy`

## Installation
```
git clone https://github.com/cjm715/mgym.git
cd mgym/
pip install -e .
 ```

## Environments
* [x] TicTacToe-v0
* [x] RockPaperScissors-v0
* [x] PrisonersDilemma-v0
* [x] BattleOfTheSexes-v0
* [x] StagHunt-v0
* [x] MatchingPennies-v0
* [ ] TravelingCheckers-v0 ([Introduced in SFI's complexity challenge](https://www.complexityexplorer.org/challenges/1-launch-of-the-complexity-challenges/submissions))
* [x] ElFarol-v0
* [ ] WolfPack-v0
* [ ] FruitGathering-v0
<!-- * [ ] Snake-v0 ([See OpenAI's Request-for-research](https://blog.openai.com/requests-for-research-2/)) -->


## Examples
```python
import gym
import mgym
import random

env = gym.make('TicTacToe-v0')
fullobs = env.reset()
while True:
    print('Player O ') if fullobs[0] else print('Player X')
    a = random.choice(env.get_available_actions())
    fullobs,rewards,done,_ = env.step(a)
    env.render()
    if done:
        break
```


```python
import gym
import mgym

env = gym.make('MatchingPennies-v0')
env.reset(3)
while True:
    a = env.action_space.sample()
    _,r,done,_ = env.step(a)
    env.render()
    if done:
        break
```

See further examples in `mgym/examples/examples.ipynb`.

## How are multi-agent environments different than single-agent environments?

When dealing with multiple agents, the environment must communicate which agent(s)
can act at each time step. This information must be incorporated into observation space.
Conversely, the environment must know which agents are performing actions. Therefore this must
be communicated in the action passed to the environment. The form of the API used for passing this information depends on the type of game. The two types are

* one-at-a-time play  (like TicTacToe, Go, Monopoly, etc) or
* simultaneous play (like Soccer, Basketball, Rock-Paper-Scissors, etc).

In the TicTacToe example above, this is an instance of one-at-a-time play. The `fullobs` is
a tuple `(next_agent, obs)`. The variable `next_agent` indicates which agent will act next.
`obs` is the typical observation of the environment state. The action `a` is also a tuple given
by `a = (acting_agent, action)` where the `acting_agent`
is the agent acting with the action given by variable `action`.

## Testing
To run tests, install pytest with `pip install pytest` and run `python -m pytest`
