import chess
from MinimaxAI import *
from ChessGame import *
from math import inf
import random

class IDSMinimaxAI():

    # initialize the minimiax
    def __init__(self, team, eval_function, time_limit):
        self.team = team
        self.eval_function = eval_function
        self.count = [0]
        self.time_limit = time_limit

    def choose_move(self, board): 
        # store the best move, remember the current depth: 
        best_move = None
        current_depth = 1

        # while the time limit hasn't been reached
        while self.count[0] < self.time_limit: 
            # run the minimax on that depth
            best_move = self.run_minimax(board, current_depth)
            print(best_move)
            print("Ordered Count:" + str(self.count))
            print("IDS Completed at Depth " + str(current_depth))
            current_depth += 1
            
        return best_move


    def run_minimax(self, board, depth):
        # get the current legal moves
        legal_moves = self.get_ordered_moves(board)
        
        # if there are no more moves, return none
        if len(legal_moves) == 0: 
            return None
        
        # otherwise, store a random move
        best_move = random.choice(legal_moves)
        max_eval = -inf # set this low so that the eval must be higher

        # remember how many nodes have been visited
        self.count = [0]

        # loop through the current legal moves
        for move in legal_moves: 
            # push that move to the board, call minimax on it, save the value and pop
            board.push(move)
            self.count[0] += 1
            minimax = self.minimax(board, depth-1, -inf, inf)
            board.pop()

            # if the value is greater than the current max: 
            if minimax >= max_eval: 
                # update the max value and save best move
                max_eval = minimax
                best_move = move
        # return the best move
        return best_move

    
    # recursive minimax algorithm
    def minimax(self, board, depth, alpha, beta, maximizing_player=False):
        self.count[0] += 1
        # base case: cutoff taest
        if self.cutoff_test(board, depth):
            # return the evaluation of the current board
            return self.eval_function(board, self.team)

        # get the next possible moves, return the board's value if none exist. 
        next_moves = self.get_ordered_moves(board)
        if next_moves == None:
            return self.eval_function(board, self.team)

        # if it is max's turn
        if maximizing_player: 
            max_eval = -inf
            # loop through all of the successor moves
            for move in next_moves:
                # push that move to the board
                board.push(move)
                # call minimax on the board with the new move and save the value
                minimax = self.minimax(board, depth-1, alpha, beta, False)
                # pop the move from the board
                board.pop()
                # update the max_eval test beta,
                max_eval = max(max_eval, minimax)
                if max_eval >= beta: return max_eval
                # update alpha
                alpha = max(alpha, max_eval)
            #return the highest value of all successors
            return max_eval

        # if it is min's turn
        else: 
            min_eval = inf # set this high so the evaluation will be lower
            # loop through all of the successor moves
            for move in next_moves:
                # push that move to the board
                board.push(move)
                # call minimax on the board with the new move and save the value
                minimax = self.minimax(board, depth-1, alpha, beta, True)
                # pop the move from the board
                board.pop()
                # update the min_eval and test alpha
                min_eval = min(min_eval, minimax)
                if min_eval <= alpha: return min_eval
                # update beta
                beta = min(beta, min_eval)
            #return the lowerst value of all successors
            return min_eval


    # cutoff test function
    def cutoff_test(self, board, depth):
        if depth == 0 or board.is_game_over():
            return True
        return False

    def get_ordered_moves(self, board):
        
        # Get all legal moves from the current position
        moves = list(board.legal_moves)
    
        # make two lists for the catpure and non-catpure moves
        capture_moves = []
        noncapture_moves = []

        # sort moves into the two lists
        for move in moves:
            if board.is_capture(move):
                capture_moves.append(move)
            else:
                noncapture_moves.append(move)
    
        # Return moves with captures first, followed by forward moves, then backward moves
        ordered_moves = capture_moves + noncapture_moves
        return ordered_moves

if __name__ == "__main__":
    pass


