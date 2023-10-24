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
    solution = sudoku_solver.walksat()
    if solution:
        print("Puzzle Solved in " + str(sudoku_solver.iterations_used) + " iterations")
        display_sudoku_solution(solution_path)
    else:
        print("No solution found within the maximum number of iterations.")


if __name__ == "__main__":

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 2000  # Maximum number of iterations

    # FOR TESTER: READ THIS: 
    # INPUT THE PATH TO THE DIRECTORY OF THE PUZZLES AND SOLUTIONS RESPECTIVELY HERE SO THE TESTS WILL PRINT TO AND FROM THE RIGHT FILE
    # - I have a directory for the whole class, so I have to specify the folder is Sudoku/solutions or Sudoku/puzzles. 
    # - For you it will likely just be /solutions/ and /puzzles/
    # 
    # ALSO: 
    # If you don't want to wait for all of these problems to run (it takes a minute or two), 
    # COMMENT OUT THE `test_walksat` functions, and leave only the display_sudoku_solution calls (below)
    # - This will just read the solution outputs from my program and display the solutions in the terminal. 


    puzzle_dir = "Sudoku/puzzles/" # probably replace this with /puzzles/
    solutions_dir = "Sudoku/solutions/" # probably replace this with /solutions/

    ## gsat tests: see solutions folder for outputs. 
    # random.seed(1)
    # test_gsat(threshold, puzzle_dir + "one_cell.cnf", solutions_dir + "one_cell_gsat_0.3.sol")
    # random.seed(1)
    # threshold = 0.5  # Random threshold for accepting non-improving moves
    # test_gsat(threshold, puzzle_dir + "all_cells.cnf", solutions_dir + "all_cells_gsat_0.5.sol")
    # threshold = 0.3  # Random threshold for accepting non-improving moves
    # random.seed(1)
    # test_gsat(threshold, puzzle_dir + "rows.cnf", solutions_dir + "rows_gsat_0.5.sol")

    ## walksat tests: see solutions folder for outputs. 
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "one_cell.cnf", solutions_dir + "one_cell_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "all_cells.cnf", solutions_dir + "all_cells_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "rows.cnf", solutions_dir + "rows_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "rows_and_cols.cnf", solutions_dir + "rows_and_cols_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "rules.cnf", solutions_dir + "rules_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "puzzle1.cnf", solutions_dir + "puzzle1_walksat_0.3.sol")
    # random.seed(1)
    # test_walksat(threshold, puzzle_dir + "puzzle2.cnf", solutions_dir + "puzzle2_walksat_0.3.sol")

    ## print the solutions from the solver outputs without running again: 
    # print("Walksat one cell; 0.3")
    # display_sudoku_solution(solutions_dir + "one_cell_walksat_0.3.sol")

    # print("Walksat all cells; 0.3")
    # display_sudoku_solution(solutions_dir + "all_cells_walksat_0.3.sol")

    # print("Walksat rows; 0.3")
    # display_sudoku_solution(solutions_dir + "rows_walksat_0.3.sol")

    # print("Walksat rows and cols; 0.3")
    # display_sudoku_solution(solutions_dir + "rows_and_cols_walksat_0.3.sol")

    # print("Walksat rules; 0.3")
    # display_sudoku_solution(solutions_dir + "rules_walksat_0.3.sol")

    # print("Walksat puzzle 1; 0.3")
    # display_sudoku_solution(solutions_dir + "puzzle1_walksat_0.3.sol")

    ## these were used to make the graphs for all cells on walksat
    # cnf_file = "all_cells.cnf"
    # random_seed = 1
    # threshold = 0.1  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.1.sol")
    # threshold = 0.2  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.2.sol")
    # threshold = 0.3  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.3.sol")
    # threshold = 0.4  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.4.sol")
    # threshold = 0.5  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.5.sol")
    # threshold = 0.6  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.6.sol")
    # threshold = 0.7  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.7.sol")
    # threshold = 0.8  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.8.sol")
    # threshold = 0.9  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.9.sol")

    # these were used to make the graphs for all cells on gsat
    cnf_file = "rules.cnf"
    threshold = 0.1  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.1.sol")
    threshold = 0.2  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.2.sol")
    threshold = 0.3  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.3.sol")
    threshold = 0.4  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.4.sol")
    threshold = 0.5  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file +"_gsat_0.5.sol")
    threshold = 0.6  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.6.sol")
    threshold = 0.7  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.7.sol")
    threshold = 0.8  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.8.sol")
    threshold = 0.9  # Random threshold for accepting non-improving moves
    random.seed(1)
    test_gsat(threshold, puzzle_dir + cnf_file, solutions_dir + cnf_file + "_gsat_0.9.sol")

    ## these were used to make the graphs for rules on walksat
    # cnf_file = "rules.cnf"
    # random_seed = 1
    # threshold = 0.1  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.1.sol")
    # threshold = 0.2  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.2.sol")
    # threshold = 0.3  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.3.sol")
    # threshold = 0.4  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.4.sol")
    # threshold = 0.5  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.5.sol")
    # threshold = 0.6  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.6.sol")
    # threshold = 0.7  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.7.sol")
    # threshold = 0.8  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.8.sol")
    # threshold = 0.9  # Random threshold for accepting non-improving moves
    # random.seed(random_seed)
    # test_walksat(threshold, puzzle_dir + "cnf_file", solutions_dir + "all_cells_walksat_0.9.sol")







