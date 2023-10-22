import random

class SAT:
    def __init__(self, cnf_file_path, solution_path, threshold, max_iterations):
        # parameters
        self.cnf_file_path = cnf_file_path
        self.solution_path = solution_path
        self.threshold = threshold
        self.max_iterations = max_iterations

        # declare the clauses, variables, and assignments lists
        self.clauses = []
        self.variables = []
        self.assignment = {}

        # initialize the clauses, variables, and assignment using the functions
        self.initialize_clauses()
        self.initialize_random_assignment()

    # initialize the clauses list
    def initialize_clauses(self):
        try:
            # Read the cnf line by line
            with open(self.cnf_file_path, 'r') as file:
                clauses = []
                for line in file:
                    # Parse elements in clause
                    clause = line.strip().split()
                    converted_clause = []

                    # loop through each variable, add it to the var list if it isn't there
                    for variable in clause: 
                        neg = False
                        # if the variable is negative, take of the negative sign
                        if variable[0] == '-': 
                            variable = variable[1:]
                            neg = True
                        # if the variable not in the variable list, add it
                        if variable not in self.variables: 
                            self.variables.append(variable)
                        if neg: 
                            converted_clause.append(-1 * (self.variables.index(variable) + 1))
                        else: 
                            converted_clause.append(self.variables.index(variable) + 1)
                    clauses.append(converted_clause)
                            
                self.clauses = clauses

        except FileNotFoundError:
            print(f"Error: File '{self.cnf_file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    # initialize the random variable assignment
    def initialize_random_assignment(self):
        # for each variable (do this by index)
        for i in range(1, len(self.variables) + 1): 
            # randomly choose positive or negative
            value = random.choice([True, False])
            # add the index to the list: positive if true and negative if false
            self.assignment[i] = value

    def count_satisfied_clauses(self):
        satisfied_clauses = 0
        # loop through clauses
        for clause in self.clauses:
            # if the entire clause is satisfied, increment the count
            for var in clause:
                if var > 0 and self.assignment[var] == True:
                    satisfied_clauses += 1
                    break
                elif var < 0 and self.assignment[-var] == False:
                    satisfied_clauses += 1
                    break
        # return the number of satisfied clauses
        return satisfied_clauses

    def gsat(self):
        for i in range(self.max_iterations):
            # get the number of satisfied clauses
            num_satisfied = self.count_satisfied_clauses()
            print(str(num_satisfied) + '/' + str(len(self.clauses)))

            # Check if the current assignment satisfies all clauses
            if num_satisfied == len(self.clauses):
                # self.write_solution()
                return self.assignment  # Solution found

            # Random number between 0 and 1
            random_threshold = random.random()
            if random_threshold > self.threshold:
                # Random Move: Flip a random variable
                random_var = random.choice(list(self.assignment.keys()))
                self.assignment[random_var] = not self.assignment[random_var]

            # if threshold wasn't reached
            else:
                # initialize the best assignment and best choices set
                best_flips = []
                max_num_satisfied = 0

                # for each variable
                for variable in list(self.assignment.keys()): 
                    # flip the variable
                    self.assignment[variable] = not self.assignment[variable]
                    # count num clauses satisfied with the new one
                    new_num_satisfied = self.count_satisfied_clauses()
                    # flip it back
                    self.assignment[variable] = not self.assignment[variable]
                    # if it's the new highest, reset the list
                    if new_num_satisfied > max_num_satisfied: 
                        # empty the list and add it to the list
                        max_num_satisfied = new_num_satisfied
                        best_flips = [variable]
                    # otherwise, if flipping that variable results in an equal score: 
                    elif new_num_satisfied == max_num_satisfied:
                        # add it to the list
                        best_flips.append(variable)

                # flip a random variable from the maximizing list
                var_to_flip = random.choice(best_flips)
                self.assignment[var_to_flip] *= -1

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

    # writes the solution to a file 
    def write_solution(self):
        try:
            # make the new file
            new_filename = self.solution_path
            with open(new_filename, 'w') as file:
                # write each of the variables to a line in a file
                for variable in self.assignmnent:
                    # if the variable is true, write it to the file
                    if variable > 0:
                        file.write(self.variables[variable-1] + '\n')
        except Exception as e:
            print(f"Error: {e}")
 

# Example usage:
if __name__ == "__main__":

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 100000  # Maximum number of iterations
    cnf_file_path = "Sudoku/puzzles/one_cell.cnf"
    solution_path = "Sudoku/solutions/one_cell.sol"

    sudoku_solver = SAT(cnf_file_path, solution_path, threshold, max_iterations)
    solution = sudoku_solver.gsat()

    if solution:
        print("Puzzle Solved:")
        print(solution)
    else:
        print("No solution found within the maximum number of iterations.")


