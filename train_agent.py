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

import random
from collections import deque
import numpy as np
from neural_network import model
from gobblers import Gobbler


memory = deque(maxlen=2000)

batch_size = 32
gamma = 0.95  # discount rate
epsilon = 1.0  # exploration rate
epsilon_decay = 0.995
epsilon_min = 0.01  # minimum exploration rate
learning_rate = 0.001   

def train(model):
    if len(memory) < batch_size:
        return
    
    batch = random.sample(memory, batch_size)

    for state, action, reward, next_state, done in batch:
        if done:
            target = reward
        else:
            # whats the higest q value for the next state
            # apply to the q value of the current state
            # why is important to consider about the gamma value?
            next_action = np.argmax(model.predict(next_state))
            target = reward + gamma * model.predict(next_state)[next_action]

        current_q = model.predict(state).copy()
        current_q[action] = target
        
        # X_train: (27,), y_train: (27,), 
        model.train(state, np.array(current_q), 100, 0.01)
        # train the model on the target values

        global epsilon
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

def select_action(state, valid_moves, model):
    # select an action based on epsilon
    # get random move, and then mask invalid moves, and then return highest q value
    if np.random.rand() <= epsilon:
        return random.choice(valid_moves)
    else:
        # make into a np array
        q_values = model.predict(state).copy()
        for i in range(len(q_values)):
            if i not in valid_moves:
                q_values[i] = -np.inf
    
    #print(q_values)
    
    return np.argmax(q_values)

def remember(state, action, reward, next_state, done):
    memory.append((state, action, reward, next_state, done))

def train_agent(episodes=1000):
    mod = model(n_input_variables=27, n_hidden_nodes=500, n_classes=27)

    for episode in range(episodes):
        if episode % 10 == 9:
            print(f"Episode {episode + 1}/{episodes}")
        game = Gobbler()
        done = False

        while not done:
            state = game.get_board()

            valid_moves = game.get_possible_moves()

            # will only return a valid move
            move = select_action(state, valid_moves, mod)

            game.make_move(move)

            game_over = game.check_game_over()

            if game_over:
                if game.get_possible_moves() == []:
                    reward = 0.5
                else:
                    reward = 1 
                done = True
            else:
                opponent_move = random.choice(game.get_possible_moves())
                game.make_move(opponent_move)

                game_over = game.check_game_over()

                if game_over:
                    if game.get_possible_moves() == []:
                        reward = 0.5
                    else:
                        reward = -1
                    done = True
                else:
                    reward = 0
                
            next_state = game.get_board()

            remember(state, move, reward, next_state, done)
            train(mod)
    return mod

if __name__ == "__main__":
    trained_model = train_agent(episodes=100)
    #trained_model.save_weights()
    #trained_model = model(n_input_variables=27, n_hidden_nodes=200, n_classes=27)
    #trained_model.load_weights()
    g = Gobbler()
    epsilon = 0
    print("Training complete.")