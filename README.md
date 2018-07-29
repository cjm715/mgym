# Multiagent gym environments

## Dependencies
* `gym`
* `numpy`

## Installation
To install package, use the following commands:
* `git clone https://github.com/cjm715/mgym.git`
* `cd mgym/`
* `pip install -e .`

## Environments
* TicTacToe-v0

## Example
```python
import gym
import mgym
import random

# initialize
env = gym.make('TicTacToe-v0')
fullobs = env.reset()
env.render()
while True:
    print('Player O ') if fullobs[0] else print('Player X')
    a = random.choice(env.get_available_actions())
    fullobs,rewards,done,_ = env.step(a)
    env.render()
    if done:
        break
```

## Testing
To run tests, install pytest with `pip install pytest` and run `python -m pytest`
