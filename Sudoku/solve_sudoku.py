from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    # puzzle_name = str(sys.argv[1][:-4])
    # sol_filename = puzzle_name + ".sol"
    # sol_filename = puzzle_name + ".sol"

    sat = SAT()
    result = sat.walksat("Sudoku/puzzle1.cnf", 1000000)

    # if a result was found, print it 
    if result:
        display_sudoku_solution(result)
    else: 
        print("No result found")