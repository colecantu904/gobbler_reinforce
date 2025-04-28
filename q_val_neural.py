import numpy as np

# to encode the board, it will need to be flattened into a 27 element vector, 
# 0 for empty space, 1, 2, 3 for your piece sizes and -1, -2 -3 for opponent pieces
# output nodes will be the Q-values for each possible action, which is at most 27
# (batch size , 27 state slots + 1 bias) x (27 state slots + 1 bias, X hidden nodes + 1 bias) x (X hidden nodes, 27 possible actions q values) = (batch size, 27 possible actions q values)
# 

