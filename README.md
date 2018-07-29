# Multiagent gym environments

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
* TicTacToe-v0

## Example
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

## How are Multi-agent environments different than Single-agent environments?

When dealing with multiple agents, the environment must communicate which agent(s)
can act at each time step. Thus, this information must be incorporated into observation space.

There are a few multi-agent game structures that are common:

* one-at-a-time play
* simultaneous play

In the TicTacToe example above, this is an instance of one-at-a-time play. The `fullobs` is
a tuple `(next_agent, obs)`. The variable `next_agent` indicates which agent will act next.
`obs` is the typical observation of the environment state. The action `a` is also a tuple given
by `a = (acting_agent, action)` where the `acting_action`
is the agent acting with the action given by variable `action`.

## Testing
To run tests, install pytest with `pip install pytest` and run `python -m pytest`
