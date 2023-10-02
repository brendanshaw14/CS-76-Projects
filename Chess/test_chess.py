# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import *
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys


player1 = HumanPlayer()
player2 = MinimaxAI(2)

game = ChessGame(player1, player2)

## run the game in the console
# while not game.is_game_over():
    # print(game)
    # print(game.evaluate_board())
    # game.make_move()


#print(hash(str(game.board)))

# Test positions with their expected evaluation values
test_positions = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0),
    ("rnbqkbn1/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 5),
    ("rnbqkbn1/ppppppp1/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 6),
    ("rnbqkb2/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 8),
    ("rnbqk3/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 11),
    ("rnb1kbn1/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 14),
    ("rnbq4/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 51),
    ("rnb1kbn1/pppppppp/8/8/8/8/3PPPPP/RNBQKBNR w KQkq - 0 1", 11),
    ("rnb1kbn1/pppppppp/8/8/8/8/3PPPPP/1NBQKBNR w KQkq - 0 1", 6),
    ("rn1qk1nr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1", -3),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RN2KBNR w KQkq - 0 1", -12),
    ("rnbqkbn1/pppppppp/8/8/8/8/PPPPPPPP/RN2KBNR w KQkq - 0 1", -7),
    ("rn1qkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK3 w KQkq - 0 1", -8),
]

# Evaluate each test position
for fen, expected_value in test_positions:
    game.board = chess.Board(fen)
    print(game.board)
    print("Expected Value:", expected_value)
    print("Evaluated Value:", evaluate_board(game.board))
    print("-" * 40)  # Separator for clarity