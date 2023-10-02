import chess
from ChessGame import *

class MinimaxAI():

    # initialize the minimiax
    def __init__(self, depth):
        self.depth = depth

    # call minimax on the moves from the current position
    # return the move with the highest minimax value
    def choose_move(self, board):
        # get the current legal moves
        legal_moves = list(board.legal_moves)
        best_move = None
        max_eval = -100 # set this low so that the eval must be higher

        # loop through the current legal moves
        for move in legal_moves: 
            # push that move to the board, call minimax on it, save the value and pop
            board.push(move)
            minimax = self.minimax(board, self.depth)
            board.pop()

            # if the value is greater than the current max: 
            if minimax > max_eval: 
                # update the max value and save best move
                max_eval = minimax
                best_move = move

        # return the best move
        return best_move

    
    # recursive minimax algorithm
    def minimax(self, board, depth, maximizing_player=True):
        # base case: if the game is over or the max depth is reached: 
        if depth == 0 or board.is_game_over():
            # return the evaluation of the current board
            return evaluate_board(board)

        # get the next possible moves 
        next_moves = list(board.legal_moves)

        # if it is max's turn
        if maximizing_player: 
            max_eval = -100
            # loop through all of the successor moves
            for move in next_moves:
                # push that move to the board
                board.push(move)
                # call minimax on the board with the new move and save the value
                minimax = self.minimax(board, depth-1, False)
                # pop the move from the board
                board.pop()
                # update the max_eval 
                max_eval = max(max_eval, minimax)
            #return the highest value of all successors
            return max_eval

        # if it is min's turn
        else: 
            min_eval = 100 # set this high so the evaluation will be lower
            # loop through all of the successor moves
            for move in next_moves:
                # push that move to the board
                board.push(move)
                # call minimax on the board with the new move and save the value
                minimax = self.minimax(board, depth-1, True)
                # pop the move from the board
                board.pop()
                # update the min_eval 
                min_eval = min(min_eval, minimax)
            #return the lowerst value of all successors
            return min_eval


if __name__ == "__main__":

    pass


    # #base case- return the current node if it has no children
    # if self.next_moves == set():
        # return self
    # #if nodes team is different or the head node: return the child with max value
    # elif self.piece == None or self.piece.color != self.team_color:
        # max_value = -1290
        # for move in self.next_moves: 
            # next_minimax = move.minimax()
            # if next_minimax.value >= max_value: 
                # max_value = next_minimax.value
                # best_move = move
        # print("best value returned: " + str(best_move.value))
        # return best_move
    # #if nodes team is the opponent, return the child with min value
    # else:
        # min_value = 1290
        # for move in self.next_moves: 
            # next_minimax = move.minimax()
            # if next_minimax.value <= min_value: 
                # min_value = next_minimax.value
                # worst_move = move
        # print("worst value returned: "+ str(worst_move.value))
        # return worst_move
            