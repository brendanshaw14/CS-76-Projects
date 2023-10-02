import chess

# define the piece values for evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9, 
    chess.KING: 40
}

class ChessGame:

    
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"

# Function to evaluate the value of the board at a given state
def evaluate_board(board):
        
    # initialize the total value to be 0   
    total_value = 0
    # for each square
    for square in chess.SQUARES:
        # get that square's piece
        piece = board.piece_at(square)
        # if there is a piece in the square 
        if piece is not None:
            # get the piece's value
            piece_value = piece_values[piece.piece_type]
            # add it to or subtract it from the total value accordingly
            if piece.color == chess.WHITE:
                total_value += piece_value
            else:
                total_value -= piece_value
    # return the board's total value 
    return total_value

