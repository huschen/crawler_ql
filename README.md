# Crawler, Q-learning
 
Visual and interactive extension of Q-learning Crawler, based on the lectures and code from [Introduction to Artificial Intelligence, UC Berkeley](http://inst.eecs.berkeley.edu/~cs188/).

The game environment is a simplified kinematic model and the size of the action space is (13*9=) 117.
The project is small and self-contained, aiming to help gain an instinctual understanding of random walk, exploitation and exploration, the convergence of Q-value.

Alternative approach to the Crawler problem: model-based learning and MDP. The transitions are deterministic and the reward for every transition is known. In Q learning, when epsilon = 1 (meaning random exploration and no exploitation), it is equivalent to value iteration of MDP but in a random order and a less sample-efficient way.

The convergence and optimality of both Q-learning (fully explored) and value-iteration policies depend on the value of the discount factor. Increasing the discount factor from 0.8 (as demonstrated below) to 0.95, results a better policy with bigger crawling velocity (simply because the velocity is calculated without discount) but much longer convergence time.

![](stable.gif)

To train the Crawler: python crawlerMain.py.
Prerequisites: Python 3.6 (tested on Mac OS X).
