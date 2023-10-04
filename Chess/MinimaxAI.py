import chess
from ChessGame import *
from EvaluateBoard import evaluate_board
from math import inf
import random

class MinimaxAI():

    # initialize the minimiax
    def __init__(self, depth, team):
        self.depth = depth
        self.team = team
        self.count = [0]

    # call minimax on the moves from the current position
    # return the move with the highest minimax value
    def choose_move(self, board):
        # get the current legal moves
        legal_moves = list(board.legal_moves)
        best_move = random.choice(legal_moves)
        max_eval = -inf # set this low so that the eval must be higher
        self.count = [0]

        # loop through the current legal moves
        for move in legal_moves: 
            # push that move to the board, call minimax on it, save the value and pop
            board.push(move)
            self.count[0] += 1
            minimax = self.minimax(board, self.depth)
            board.pop()

            # if the value is greater than the current max: 
            if minimax >= max_eval: 
                # update the max value and save best move
                max_eval = minimax
                best_move = move
        print("Minimax Count: " + str(self.count))
        # return the best move
        return best_move

    
    # recursive minimax algorithm
    def minimax(self, board, depth, maximizing_player=False):
        self.count[0] += 1
        # base case: if the game is over or the max depth is reached: 
        if depth == 0 or board.is_game_over():
            # return the evaluation of the current board
            return evaluate_board(board, self.team)

        # get the next possible moves, return the board's value if none exist. 
        next_moves = list(board.legal_moves)
        if next_moves == None:
            return evaluate_board(board, self.team)

        # if it is max's turn
        if maximizing_player: 
            max_eval = -1000
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
            min_eval = 1000 # set this high so the evaluation will be lower
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


