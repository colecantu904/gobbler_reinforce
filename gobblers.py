# make an object that can:
# 1. give the current gamestate
# 2. give the current possible moves
# 3. give the current player
# 4. make a move
# 5. check if the game is over
# 6. give the move history

# keep in mind, design so that you can play against a human or a computer!

# board is a 3x3 grid:
# [[[], [], []],
# [[], [], []],
# [[], [], []]]
# need to remake board in encoded object, for the prediction model?
# ALL OF THIS LOGIC SHOULD BE ON ENCODED DATA, AND THEN DECODED FOR INDIVUDAL APPLICATION
# NEED TO MAKE HE BOARD A 1-D ARRAY, THE VALID MOVES INTEGERS (0 - 26)
# MAKE AN DECODE METHOD, TO TURN IT BACK INTO A 3X3 GRID, AND KEEP ORIGINAL GET MOVES
import numpy as np

class Gobbler:
    def __init__(self):
        self.board = np.zeros(27, dtype=int)
        self.move_history = []
        # 1 for first plater and -1 for second player
        self.current_player = 1
        # [[ small, medium, large],[small, medium, large]]
        self.available_pieces = [[ 2 for _ in range(3)], [ 2 for _ in range(3)]]
        self.game_over = False

    def __str__(self):
        board_str = ""
        j = 0
        for i in range(2, 29 ,3):
            if j % 3 == 2:
                board_str += f"[{i - 2}. {self.board[i - 2]} {i - 1}. {self.board[i - 1]} {i}. {self.board[i]}]\n"
            else:
                board_str += f"[{i - 2}. {self.board[i - 2]} {i - 1}. {self.board[i - 1]} {i}. {self.board[i]}]"
            j += 1
        return board_str
    
    def get_board(self):
        return self.board.copy()
    
    def get_current_player(self):
        # 0 for player 1, 1 for player 2
        return self.current_player

    def get_possible_moves(self):
        # for each cell
        valid_moves = []
        if self.current_player == 1:
            current_player = 0
        else:
            current_player = 1
        for i in range(2, 29 ,3):
            # starting from the largest piece, i + 2, then down
            if self.board[i] == 0:
                if self.available_pieces[current_player][2] > 0:
                    valid_moves.append(i)
                if self.board[i - 1] == 0 and self.board[i] == 0:
                    if self.available_pieces[current_player][1] > 0:
                        valid_moves.append(i - 1)
                    if self.board[i - 2] == 0 and self.board[i - 1] == 0:
                        if self.available_pieces[current_player][0] > 0:
                            valid_moves.append(i - 2)
        return valid_moves
                    
    def make_move(self, move):
        if not self.game_over:
            if self.current_player == 1:
                current_player = 0
            else:
                current_player = 1
            self.available_pieces[current_player][move % 3] -= 1
            self.board[move] = self.current_player
            self.current_player = self.current_player * -1
            self.move_history.append(move)

            if self.check_game_over():
                self.game_over = True


    # [[0, 1, 2], [3, 4, 5], [6, 7, 8],
    # [9, 10, 11], [12, 13, 14], [15, 16, 17],
    # [18, 19, 20], [21, 22, 23], [24, 25, 26]]
    def check_game_over(self):
        # this one is tough, need some way to chcek the largest piece with winning combinoations
        # need some expression to check if the game is overs
        effective = []
        for tile in range(9):
            small = self.board[tile * 3 + 0]
            medium = self.board[tile * 3 + 1]
            large = self.board[tile * 3 + 2]
            
            # Prioritize large > medium > small
            if large != 0:
                effective.append(large)
            elif medium != 0:
                effective.append(medium)
            else:
                effective.append(small)

        # Now check for a win (either 1 or -1 three in a row)
        win = (
            (effective[0] != 0 and effective[0] == effective[1] == effective[2]) or
            (effective[3] != 0 and effective[3] == effective[4] == effective[5]) or
            (effective[6] != 0 and effective[6] == effective[7] == effective[8]) or
            (effective[0] != 0 and effective[0] == effective[3] == effective[6]) or
            (effective[1] != 0 and effective[1] == effective[4] == effective[7]) or
            (effective[2] != 0 and effective[2] == effective[5] == effective[8]) or
            (effective[0] != 0 and effective[0] == effective[4] == effective[8]) or
            (effective[2] != 0 and effective[2] == effective[4] == effective[6])
        ) or self.get_possible_moves() == []

        return win
        
    def get_winner(self):
        if self.game_over:
            if self.get_possible_moves() == []:
                return 0.5
            return self.current_player * -1
        return None
    
    def reset(self):
        self.board = [0 for _ in range(27)]
        self.move_history = []
        self.current_player = 1
        self.available_pieces = [[2 for _ in range(3)], [2 for _ in range(3)]]
        self.game_over = False



class gobbler:
    def __init__(self):
        self.board = [[[] for _ in range(3)] for _ in range(3)]
        self.move_history = []

    def get_board(self):
        return self.board
    
    def _get_available_pices(self):
        available_pieces = {('b', 0) : 2, ('b', 1) : 2, ('b', 2) : 2,
                            ('r', 0) : 2, ('r', 1) : 2, ('r', 2) : 2,}
        for i in range(3):
            for j in range(3):
                # if the piece is not empty, remove it from the available pieces
                # and decrease the count of that piece
                for piece in self.board[i][j]:
                        available_pieces[piece] -= 1
        return available_pieces
    
    def get_current_player(self):
        # dependeing on the current state of the board, return the current player
        # if the board is empty, return 'b'
        player1 = 0
        player2 = 0
        for i in range(3):
            for j in range(3):
                for piece in self.board[i][j]:
                    if piece[0] == 'b':
                        player1 += 1
                    else:
                        player2 += 1
        if player1 > player2:
            return 'r'
        else:
            return 'b'

    # this is a little buggy, check to make sure its good.
    def get_possible_moves(self):
        possible_moves = []
        available_pieces = self._get_available_pices()
        current_player = self.get_current_player()
        for i in range(3):
            # if piece is available and the current piece is smaller or empty
            for j in range(3):
                for piece in available_pieces:
                    # if the piece is available
                    if current_player == piece[0]:
                        if available_pieces[piece] > 0:
                            if self.board[i][j] == [] or (self.board[i][j] != [] and self.board[i][j][-1][1] < piece[1]):
                                possible_moves.append((piece, (i, j)))
        return possible_moves
    
    def make_move(self, move):
        # move is a tuple of (piece, position)
        # input is in form: (('player_color', piece_size), position)
        # if move in self.get_possible_moves():
        piece, position = move
        self.board[position[0]][position[1]].append(piece)
        self.move_history.append(move)
        # check if the game is over

    # maybe should just have this return a boolean
    # and have the check_game_over function return the winner
    def check_game_over(self):
        # i am pretty sure this is correct, but its so tedious to try every combination!
        # and don't get on me about the long boolean expression, its just how it is
        # check horizantal:
        for i in range(3):
            if self.board[i][0] != [] and self.board[i][1] != [] and self.board[i][2] != [] and self.board[i][0][-1][0] == self.board[i][1][-1][0] == self.board[i][2][-1][0]:
                return self.board[i][0][-1][0]
        # check vertical:
        for i in range(3):
            if self.board[0][i] != [] and self.board[1][i] != [] and self.board[2][i] != [] and self.board[0][i][-1][0] == self.board[1][i][-1][0] == self.board[2][i][-1][0]:
                return self.board[0][i][-1][0]
        # check diagonals:
        if self.board[0][0] != [] and self.board[1][1] != [] and self.board[2][2] != [] and self.board[0][0][-1][0] == self.board[1][1][-1][0] == self.board[2][2][-1][0]:
            return self.board[0][0][-1][0]
        if self.board[0][2] != [] and self.board[1][1] != [] and self.board[2][0] != [] and self.board[0][2][-1][0] == self.board[1][1][-1][0] == self.board[2][0][-1][0]:
            return self.board[0][2][-1][0]

        # then its a tie
        if self.get_possible_moves() == []:
            return "Tie!"
        
        return None


    def get_move_history(self):
        return self.move_history