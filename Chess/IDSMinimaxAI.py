import chess
from MinimaxAI import *
from ChessGame import *
from math import inf
import random

class IDSMinimaxAI():

    # initialize the minimiax
    def __init__(self, depth):
        self.depth = depth

    # call minimax using IDS to find a move within the time constraint
    # return the move with the highest minimax value
    def choose_move(self, board):
        pass