from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 100000  # Maximum number of iterations
    cnf_file_path = "Sudoku/puzzles/rules.cnf"
    solution_path = "Sudoku/solutions/rules.sol"

    sudoku_solver = SAT(cnf_file_path, solution_path, threshold, max_iterations)
    # solution = sudoku_solver.gsat()
    solution = sudoku_solver.walksat()

    if solution:
        print("Puzzle Solved in " + str(sudoku_solver.iterations_used) + " iterations")
        display_sudoku_solution(solution_path)
    else:
        print("No solution found within the maximum number of iterations.")
