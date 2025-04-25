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
# env: the environment to train on
# Q-table: a table to store the Q-values for each state-action pair
# policy: a table to store the policy for each state
