from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget

import sys
import chess, chess.svg
import random

from EvaluateBoard import *
from RandomAI import RandomAI
from MinimaxAI import *
from OrderedAlphaBetaAI import *
from AlphaBetaAI import *
from IDSMinimaxAI import * 
from ChessGame import ChessGame
from HumanPlayer import HumanPlayer
from TranspositionAB import *


class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()


    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)


    def make_move(self):

        print("making move, white turn " + str(self.game.board.turn))

        self.game.make_move()
        self.display_board()




if __name__ == "__main__":


    # TO WATCH GAMEPLAY, UNCOMMENT ONE PLAYER 1 AND ONE PLAYER 2, THEN RUN THE FILE. LOGICAL MATCHUPS ARE BELOW. 

    ## Minimax Vs Random AI, depth 2
    # player1 = Minimax(2, True)
    # player2 = RandomAI()

    ## Minimax Vs Random AI, depth 3
    # player1 = Minimax(3, True)
    # player2 = RandomAI()

    ## AlphaBeta Vs Random AI, depth 2
    # player1 = AlphaBetaAI(2, True)
    # player2 = RandomAI()   

    ## AlphaBeta Vs Random AI, depth 3
    # player1 = AlphaBetaAI(3, True)
    # player2 = RandomAI()   

    ## AlphaBeta Vs Minimax
    # player1 = AlphaBetaAI(3, True)
    # player2 = Minimax(2, False)   

    ## OrderedAlphaBeta Vs RandomAI
    # player1 = OrderedAlphaBetaAI(3, True, evaluate_board_modified)
    # player2 = RandomAI()


    # testing the non-positional evaluation funciton
    # player1 = OrderedAlphaBetaAI(3, True, evaluate_board)
    # player2 = RandomAI()

    # testing the positional evaluation function: 
    # player1 = OrderedAlphaBetaAI(4, True, evaluate_board_modified)
    # player2 = RandomAI()
    
    # testing the transposition table AI:
    # player1 = TranspositionABAI(4, True, evaluate_board_modified)
    # player1 = OrderedAlphaBetaAI(4, True, evaluate_board_modified)
    # player2 = OrderedAlphaBetaAI(2, False, evaluate_board)


    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
