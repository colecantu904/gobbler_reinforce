### Todo:
- [x] Make working Gobblers implementation
- [ ] Fully test Gobbler implementation
- [x] Make a cool web ui with flask!
- [ ] Begin making Q Learning algorithim script
- [ ] Begin writing 1000 word summary (on this document)

## Notes
- You can run the flask app with `flask run` in the project directory

## Approach
We will be using an unsupervised reinforcment learning algorithim based on Q Learning.
See [this claude conversation](https://claude.ai/share/453931de-cc7d-4161-bf4d-050862636657) for a basic refernce.
Since the game is a complex enviorment with many different states, the best approach will be to approximate the Q Value function using a neural network.
If this becomes too complicated, just make a simple Q-Learning with a full Q-table for tic tac toe.

## Reward Shaping
Small intermediate rewards (values between 0 and 1):
1. three in a row of own color
2. prevent opponent three in a row
3. two in row of own color

But probably just 1 for winning, 0 for tie, and -1 for losing