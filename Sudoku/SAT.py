import random

class SAT:
    def __init__(self, cnf_file_path, threshold, max_iterations):
        self.cnf_file_path = cnf_file_path
        self.num_variables = 81
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.variable_assignments = {}
        self.clauses = self.initialize_clauses()

    # initialize the clauses list
    def initialize_clauses(self):
        try:
            with open(self.cnf_file_path, 'r') as file:
                # Read each line of the file into a list
                clauses = file.readlines()
            # Remove leading and trailing whitespace characters from each line
            cleaned_clauses = [clause.strip() for clause in clauses]
            return cleaned_clauses
        except FileNotFoundError:
            print(f"Error: File '{self.cnf_file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    # initialize the random variable assignment
    def initialize_random_assignment(self):
        return {variable: random.randint(1, 9) for variable in range(1, self.num_variables + 1)}

    # TODO: get the number of satisfied clauses
    def count_satisfied_clauses(self):
        satisfied_clauses = 0
        for clause in self.clauses:
            if any(var * (1 if self.variable_assignments[abs(var)] > 0 else -1) in clause for var in clause):
                satisfied_clauses += 1
        return satisfied_clauses

    def gsat(self, max_iterations):
        for _ in range(max_iterations):
            if self.count_satisfied_clauses() == len(self.clauses):
                return self.variable_assignments  # Solution found
            var_to_flip = random.randint(1, self.num_variables)
            original_value = self.variable_assignments[var_to_flip]
            self.variable_assignments[var_to_flip] = random.randint(1, 9)
            satisfied_clauses_after_flip = self.count_satisfied_clauses()

            if satisfied_clauses_after_flip < len(self.clauses):
                # Calculate a random threshold between 0 and 1
                random_threshold = random.random()
                if random_threshold > self.threshold:
                    # Revert the flip if the threshold is not met
                    self.variable_assignments[var_to_flip] = original_value

        return None  # No solution found within max_iterations

# Example usage:
if __name__ == "__main__":

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 10000  # Maximum number of iterations

    sudoku_solver = SAT("Sudoku/puzzle1.cnf", threshold, max_iterations)
    # solution = sudoku_solver.gsat(max_iterations)
    print(sudoku_solver.initialize_random_assignment())

    # if solution:
        # print("Sudoku Puzzle Solved:")
        # for row in range(1, 10):
            # print(" ".join(str(solution[row * 10 + col]) for col in range(1, 10)))
    # else:
        # print("No solution found within the maximum number of iterations.")
