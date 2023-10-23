from display import display_sudoku_solution
import random, sys
from SAT import SAT

def test_gsat(threshold, cnf_file_path, solution_path):
    sudoku_solver = SAT(cnf_file_path, solution_path, threshold, max_iterations)
    solution = sudoku_solver.gsat()
    if solution:
        print("Puzzle Solved in " + str(sudoku_solver.iterations_used) + " iterations")
        display_sudoku_solution(solution_path)
    else:
        print("No solution found within the maximum number of iterations.")

def test_walksat(threshold, cnf_file_path, solution_path):
    sudoku_solver = SAT(cnf_file_path, solution_path, threshold, max_iterations)
    solution = sudoku_solver.gsat()
    if solution:
        print("Puzzle Solved in " + str(sudoku_solver.iterations_used) + " iterations")
        display_sudoku_solution(solution_path)
    else:
        print("No solution found within the maximum number of iterations.")


if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 100000  # Maximum number of iterations

    # FOR TESTER: READ THIS: 
    # INPUT THE PATH TO THE DIRECTORY OF THE PUZZLES AND SOLUTIONS RESPECTIVELY HERE SO THE TESTS WILL PRINT TO AND FROM THE RIGHT FILE
    # - I have a directory for the whole class, so I have to specify the folder is Sudoku/solutions or Sudoku/puzzles. 
    # - For you it will likely just be /solutions and /puzzles
    puzzle_dir = "Sudoku/puzzles/"
    solutions_dir = "Sudoku/puzzles/"


    # walksat tests: see solutions folder for outputs. 
    test_walksat(threshold, "Sudoku/puzzles/one_cell.cnf", "Sudoku/solutions/one_cell_walksat_0.3")
    test_walksat(threshold, "Sudoku/puzzles/all_cells.cnf", "Sudoku/solutions/all_cells_walksat_0.3")
    test_walksat(threshold, "Sudoku/puzzles/rows_and_cols.cnf", "Sudoku/solutions/rows_and_cols_walksat_0.3")
    test_walksat(threshold, "Sudoku/puzzles/rules.cnf", "Sudoku/solutions/rules_walksat_0.3")

    # print the solutions from the solver outputs without running again: 
    print("Walksat one cell; 0.5")
    display_sudoku_solution()


