# we want to have a place to output Q-table and policy
# and also to have a place to output the results of the training


# parameters:
# alpha: learning rate 
# gamma: discount factor
# epsilon: exploration rate -> probability to choose a random action
# epsilon_decay: decay rate for epsilon
# epsilon_min: minimum value for epsilon
# n_episodes: number of episodes to train
# max_steps: maximum number of steps per episode
# Q-table: a table to store the Q-values for each state-action pair
# policy: a table to store the policy for each state

# we will make a nerual network to approximate the Q-values
# the input nodes will be the state, and the output nodes will be the Q-values for each possible action
# need to encode the state as a vecor, with all possible spaces for a piece, it will have 27 slots
# the maximum amount of possible acitons will ever be 27, placing any of the 3 pices on any of the 9 spaces
# (M examples, 27 state slots + 1 player identifier + 1 bias) x (27 state slots + 1 player identifier + 1 bias, X hidden nodes + 1 bias) x (X hidden nodes, 27 possible actions) = (M examples, 27 possible actions)

