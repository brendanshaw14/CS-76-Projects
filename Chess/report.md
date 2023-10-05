# Chess AI Report

## Introduction: 

Thanks to python's `chess`  library, no time was spent implementing the structure of the game itself. This project focuses on the different strategy approaches I used in the project to design and enhance the chess ai. 

## Evaluation Function

Before writing the algorithms to search the game states, I needed to develop a way to evaluate the board. I began this by using material evaluation, using the values 1, 3, 3, 5, and 9 for the pawn, knight, bishop, rook, and queen respectively.  

I needed to make the kings value higher than all of the others combined, so I just set it to 100. Of course, the evaluation of the board is then calculated by finding the difference in material value on each side. 

The algorithm is pretty simple, and can be found in the file `EvaluateBoard.py`. This function specifically is called `evaluate_board` (not `evaluate_board_modified`). 

The pseudo is as follows: 
```
def evaluate_board(board, team):
    initialize the total value to be 0   
    for each square
    for square in the board:
        get that square's piece
        if there is a piece in the square 
            get the piece's value
            if the piece is on the same team, add the value 
            otherwise, subtract the value
    return the board's total value 
```

### Evaluation Extra-Credit
Upon running the program many times though, I realized that this lead to a lot of illogical playmaking, so I searched online for some ways to improve the evaluation function. I found a strategy using positional based evaluations: the piece's position on the board is evaluated in addition to it's material value. These positional values are stored in a 2D-Array called a piece-square table. 

The algorithm looks pretty similar to the evaluation function, but adjusts the value of the piece according to where it is on the board. I found a set of piece-square tables online that would allow me to make these adjustments, and created the separate file `EvaluateBoard.py` to store the tables and separate the functions more easily. The function that uses the piece-square values is called

The tables are different for each piece: for example, here are the tables for both the knight and bishop: 
```
knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
```
```
bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
```
I read multiple articles and studies on positional evaluation and found that neural-network position systems have become increasingly popular, but I don't have much experience with that, so I decided to just use these example tables that I found. 

Since these values are obviously much larger than the material values I was using previously, I decided to change the material values rather than changing the all of the tables (for obvious reasons.) This way, it is impossible for the possition of a piece to outweight its material value.  

Here are the udpated material values: 
```
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900, 
    chess.KING: 20000
}
```
For example, a knight at the position c3 has a value of 310, whereas a knight at the position a1 has a value of 250. 

I tested that these values were being added correctly with print statements, and then continued by observing the gameplay. In comparison to the algorithms using the unmodified evaluation function, the programs using teh modified evaluation clearly prioritized controlling the center of the board. 

I also assessed the number of states visited in each search by the function before and after the implementation of positional evaluation. The algorithms visited significantly less states, because the more precise evaluations allowed for much more effective alpha beta pruning. 

## Minimax

The basic underlying strategy of the program is the `minimax` algorithm, which effectively returns the play that has the ideal worst-case outcome, reducing the chance of any pieces being captured or the game being lost, and prioritizing plays that force a capture. This is done by searching the game tree and evaluating the game state after each move. The minimax algorithm handles who's turn it is on the board differently: if it's the opposing player's (the one attmepting to minimize the board's evaluation score) turn, the minimax searches the possible moves from that state, returning the move with the lowest score. This is because we assume optimal play from the opposing player-- if there is a move that will minimize our score, we assume they will choose it. If the minimax is evaluating the maximizing player's turn, it then searches for the best possible evaluation score of those children. 

The effect is that the minimax finds the move that allows for the least possible damage to the maximizing player. 

The algorithm terminates when the `cutoff_state` is satisfied. As of now, I've set this to return true when the maximum depth of the minimax is reached or the game is over. 

## Testing Minimax: 

I started by running the minimax at different depths against the random ai. I've run minimax on a chessboard before, and the runtimes were the same as previously, which was a good sign. I tried unning the minimax on depths 1-3 against the RandomAI and used print statements to ensure that the minimax was evaluating correctly. I debugged this for a bit, and the minimax worked perfectly-- it captured pieces when available, played defensively, and always quickly and easily captured a win. However, this was only running on depths of 2 and 3, and 3 even took a fair amount of time. 

I tried this multiples times with different random seeds, depth levels, and also pitted the minimax against itself to see how it would perform. 

Here are some of the outputs from the minimax at depth 2 (random seed 1): 
```
making move, white turn True
Minimax Count: [9342]
making move, white turn False
Random AI recommending move b7b5
making move, white turn True
Minimax Count: [12130]
making move, white turn False
Random AI recommending move f7f6
making move, white turn True
Minimax Count: [13462]
making move, white turn False
Random AI recommending move e7e5
making move, white turn True
Minimax Count: [17496]
making move, white turn False
Random AI recommending move g7g6
making move, white turn True
Minimax Count: [19812]
```
And depth 3: 
```
making move, white turn True
Minimax Count: [206623]
making move, white turn False
Random AI recommending move b7b5
making move, white turn True
Minimax Count: [286114]
making move, white turn False
Random AI recommending move g7g6
making move, white turn True
Minimax Count: [296250]
making move, white turn False
Random AI recommending move g6g5
making move, white turn True
Minimax Count: [469522]
making move, white turn False
Random AI recommending move c7c6
making move, white turn True
Minimax Count: [633696]
```