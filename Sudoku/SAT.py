import random

class SAT:
    def __init__(self, cnf_file_path, solution_path, threshold, max_iterations):
        # parameters
        self.cnf_file_path = cnf_file_path
        self.solution_path = solution_path
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.iterations_used = 0
        # initialize lists
        self.clauses = []
        self.variable_assignments = {}
        self.unsatisfied_clauses = []

        # call functions
        self.initialize_clauses()
        self.initialize_random_assignment()

    # initialize the clauses list
    def initialize_clauses(self):
        try:
            # Read the cnf line by line
            with open(self.cnf_file_path, 'r') as file:
                clauses = []
                for line in file:
                    # Split the line into individual elements (numbers)
                    elements = line.strip().split()
                    # Parse elements and add them to the clauses list
                    clauses.append(list(elements))
                # set instance variable
                self.clauses = clauses

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
                # if the variable is negative, make it positive
                if variable[0] == '-': variable = variable[1:]
                # if the variable isn't in the assignment, set it to a random value
                if variable not in assignment:
                    assignment[variable] = random.choice([True, False])
        self.variable_assignments = assignment

    def count_satisfied_clauses(self):
        # initialize satisfied_clauses
        satisfied_clauses = 0
        self.unsatisfied_clauses = []
        # loop through clauses
        for clause in self.clauses:
            is_clause_satisfied = False
            # loop through variables in the clause
            for variable in clause:
                # if the variable is negative
                if variable[0] == '-':
                    # if that variable's value is false
                    if not self.variable_assignments[variable[1:]]:
                        is_clause_satisfied = True
                        break
                # if the variable is positive
                else: 
                    # if that variable's value is true
                    if self.variable_assignments[variable]:
                        is_clause_satisfied = True
                        break
            # if the entire clause is satisfied, increment the count
            if is_clause_satisfied:
                satisfied_clauses += 1
            # if not, update unsatisfied clauses list
            else: self.unsatisfied_clauses.append(clause)
        # return the number of satisfied clauses
        return satisfied_clauses

    def gsat(self):
        with open(self.solution_path[:-4] + "_progress.txt", "w") as file:
            for i in range(self.max_iterations):
                # get new num_satisfied and print it for observation
                num_satisfied = self.count_satisfied_clauses()
                progress = f"{num_satisfied}/{len(self.clauses)}"
                print(progress)  # Print to console
                file.write(progress + "\n")  # Write to file

                # Check if the current assignment satisfies all clauses
                if num_satisfied == len(self.clauses):
                    self.iterations_used = i
                    self.write_solution()
                    return self.variable_assignments  # Solution found

                # Random number between 0 and 1
                random_threshold = random.random()
                if random_threshold > self.threshold:
                    # Random Move: Flip a random variable
                    random_var = random.choice(list(self.variable_assignments.keys()))
                    self.variable_assignments[random_var] = not self.variable_assignments[random_var]

                # if threshold wasn't reached
                else:
                    # Flip a variable that maximizes the number of satisfied clauses
                    # initialize the best assignment and best choices set
                    best_flips = []
                    max_num_satisfied = 0

                    # for each variable
                    for variable in self.variable_assignments:
                        # flip the variable
                        self.variable_assignments[variable] = not self.variable_assignments[variable]
                        # count num clauses satisfied with the new one
                        new_num_satisfied = self.count_satisfied_clauses()
                        # flip it back
                        self.variable_assignments[variable] = not self.variable_assignments[variable]
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
                    self.variable_assignments[var_to_flip] = not self.variable_assignments[var_to_flip]

            return None  # No solution found within max_iterations


    def walksat(self):
        with open("progress.txt", "w") as file:
            for i in range(self.max_iterations):
                # get new num_satisfied and print it for observation
                num_satisfied = self.count_satisfied_clauses()
                progress = f"{num_satisfied}/{len(self.clauses)}"
                print(progress)  # Print to console
                file.write(progress + "\n")  # Write to file
                # if the assignment is complete:
                if num_satisfied == len(self.clauses):
                    # return the assignments as current
                    self.iterations_used = i
                    self.write_solution()
                    return self.variable_assignments

                # choose a random unsatisfied clause
                random_clause = random.choice(self.unsatisfied_clauses)

                # Random number between 0 and 1
                random_threshold = random.random()
                if random_threshold > self.threshold:
                    # Random Move: Flip a random variable from the unsatisfied clause
                    random_var = random.choice(random_clause)
                    if random_var[0] == '-': random_var = random_var[1:]
                    self.variable_assignments[random_var] = not self.variable_assignments[random_var]

                # otherwise, loop through candidates and flip the best value
                best_flips = []
                max_num_satisfied = 0
                for variable in random_clause:
                    # ditch the sign
                    if variable[0] == '-': variable = variable[1:]
                    # flip the variable
                    self.variable_assignments[variable] = not self.variable_assignments[variable]
                    # count num clauses satisfied with the new one
                    new_num_satisfied = self.count_satisfied_clauses()
                    # flip it back
                    self.variable_assignments[variable] = not self.variable_assignments[variable]
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
                self.variable_assignments[var_to_flip] = not self.variable_assignments[var_to_flip]
            # No solution found within max_iterations
            return None  

    # writes the solution to a file 
    def write_solution(self):
        try:
            # make the new file
            new_filename = self.solution_path
            with open(new_filename, 'w') as file:
                # write each of the variables to a line in a file
                for variable, assignment in self.variable_assignments.items():
                    # if the variable is true, write it to the file
                    if assignment:
                        file.write(str(variable) + '\n')
        except Exception as e:
            print(f"Error: {e}")
 

# Example usage:
if __name__ == "__main__":

    threshold = 0.3  # Random threshold for accepting non-improving moves
    max_iterations = 100000  # Maximum number of iterations
    cnf_file_path = "Sudoku/puzzles/all_cells.cnf"
    solution_path = "Sudoku/solutions/all_cells.sol"

    sudoku_solver = SAT(cnf_file_path, solution_path, threshold, max_iterations)
    print(sudoku_solver.clauses)
    print(sudoku_solver.variable_assignments)
    solution = sudoku_solver.gsat()

    if solution:
        print("Puzzle Solved in " + sudoku_solver.iterations_used + " iterations")
        print(solution)
    else:
        print("No solution found within the maximum number of iterations.")


