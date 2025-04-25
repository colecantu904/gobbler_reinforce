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

class Gobbler:
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
        print("Available pieces: ", available_pieces)
        print("Possible moves: ", possible_moves)
        return possible_moves
    
    def make_move(self, move):
        # move is a tuple of (piece, position)
        # input is in form: (('player_color', piece_size), position)
        if move in self.get_possible_moves():
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