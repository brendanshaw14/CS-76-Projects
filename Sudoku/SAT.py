import random

class SAT:
    def __init__(self, cnf_file_path, threshold, max_iterations):
        # parameters
        self.cnf_file_path = cnf_file_path
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.clauses = self.initialize_clauses()
        self.variable_assignments = self.initialize_random_assignment()

    # initialize the clauses list
    def initialize_clauses(self):
        try:
            # Read the Sudoku CNF file line by line
            with open(self.cnf_file_path, 'r') as file:
                clauses = []
                for line in file:
                    # Split the line into individual elements (numbers)
                    elements = line.strip().split()

                    # Parse elements and add them to the clauses list
                    clause = [int(element) for element in elements]
                    clauses.append(clause)
                return clauses

        except FileNotFoundError:
            print(f"Error: File '{self.cnf_file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    # initialize the random variable assignment
    def initialize_random_assignment(self):
        assignment = {}
        # for each clause line
        for clause in self.clauses:
            # for each variable
            for variable in clause:
                # set that variable to a random value
                assignment[variable] = random.choice([True, False])
        return assignment


    # TODO: get the number of satisfied clauses
    def count_satisfied_clauses(self):
        satisfied_clauses = 0
        # loop through clauses
        for clause in self.clauses:
            # loop through variables in the clause
            for var in clause: 
                # if the variable is positive
                if var >= 0: 
                    # if that variable's value is true
                    if self.variable_assignments[var] == True:
                        # increment the count, break the loop
                        satisfied_clauses += 1
                        break
                # if the variable is negative
                if var < 0: 
                    # if that variable's value is false
                    if self.variable_assignments[var] == False:
                        # increment the count, break the loop
                        satisfied_clauses += 1
                        break
        # return the number of satisfied clauses
        return satisfied_clauses

    def gsat(self):
        for i in range(self.max_iterations):
            # if the assignment is complete: 
            if self.count_satisfied_clauses() == len(self.clauses):
                # return the assignments as current
                return self.variable_assignments  
            # otherwise, randomly choose a variable and flip it 
            random_variable = random.choice(list(self.variable_assignments.keys()))
            self.variable_assignments[random_variable] = not self.variable_assignments[random_variable]

            # find the number of clauses satisfied after the flip 
            num_satisfied_after_flip = self.count_satisfied_clauses()
            
            # if it went down:
            if num_satisfied_after_flip < len(self.clauses):
                # Calculate a random threshold between 0 and 1
                random_threshold = random.random()
                if random_threshold > self.threshold:
                    # Revert the flip if the threshold is not met
                    self.variable_assignments[random_variable] = self.variable_assignments[random_variable]

        return None  # No solution found within max_iterations

    def walksat(self):
        for _ in range(self.max_iterations):
            # if the assignment is complete:
            if self.count_satisfied_clauses() == len(self.clauses):
                # return the assignments as current
                return self.variable_assignments

            # randomly choose a clause
            random_clause = random.choice(self.clauses)
            flip_variable = None
            max_satisfied_clauses = 0

            # loop through variables in the randomly chosen clause
            for var in random_clause:
                temp_assignments = self.variable_assignments.copy()
                temp_assignments[var] = not temp_assignments[var]
                num_satisfied_clauses = sum(
                    [1 for clause in self.clauses if any(
                        [temp_assignments[abs(lit)] if lit > 0 else not temp_assignments[abs(lit)] for lit in clause])])

                # if flipping the variable results in more satisfied clauses, update the flip_variable
                if num_satisfied_clauses > max_satisfied_clauses:
                    max_satisfied_clauses = num_satisfied_clauses
                    flip_variable = var

            # Calculate a random threshold between 0 and 1
            random_threshold = random.random()
            if random_threshold > self.threshold and flip_variable is not None:
                # Flip the variable if the threshold is met and a valid variable to flip is found
                self.variable_assignments[flip_variable] = not self.variable_assignments[flip_variable]

        return None  # No solution found within max_iterations
# Example usage:
if __name__ == "__main__":

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 100000  # Maximum number of iterations
    file_path = "Sudoku/one_cell.cnf"
    file_path = "Sudoku/puzzle1.cnf"
    file_path = "Sudoku/all_cells.cnf"

    sudoku_solver = SAT(file_path, threshold, max_iterations)
    solution = sudoku_solver.walksat()

    if solution:
        print("Sudoku Puzzle Solved:")
        print(solution)
    else:
        print("No solution found within the maximum number of iterations.")


