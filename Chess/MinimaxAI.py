import chess

class MinimaxAI():

    # initialize the minimiax
    def __init__(self, depth):
        self.depth = depth

    # run minimax and choose the move
    def choose_move(self, board):
        # get the current legal moves
        legal_moves = list(board.legal_moves)
        best_move = None
        max_eval = float('-inf') if board.turn == chess.WHITE else float('inf')
    
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, self.depth - 1, not board.turn)
            board.pop()
            if (board.turn == chess.WHITE and eval > max_eval) or (board.turn == chess.BLACK and eval < max_eval):
                max_eval = eval
                best_move = move
    
        return best_move


if __name__ == "__main__":
    pass

def minimax(self):
    #base case- return the current node if it has no children
    if self.next_moves == set():
        return self
    #if nodes team is different or the head node: return the child with max value
    elif self.piece == None or self.piece.color != self.team_color:
        max_value = -1290
        for move in self.next_moves: 
            next_minimax = move.minimax()
            if next_minimax.value >= max_value: 
                max_value = next_minimax.value
                best_move = move
        print("best value returned: " + str(best_move.value))
        return best_move
    #if nodes team is the opponent, return the child with min value
    else:
        min_value = 1290
        for move in self.next_moves: 
            next_minimax = move.minimax()
            if next_minimax.value <= min_value: 
                min_value = next_minimax.value
                worst_move = move
        print("worst value returned: "+ str(worst_move.value))
        return worst_move
            