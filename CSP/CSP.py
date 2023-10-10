# Constraint Satisfaction Problem Class

class CSP:
    # constructor
    def __init__(self, csp):
        self.csp = csp

        
    # returns true if all variables have been assigned
    def is_solved(self): 
        pass

    # Backtracking Algorithm
    def backtrack(self, assignment={}):
        # If the assignment is complete, return it as a solution.
        if self.csp.is_assignment_complete(assignment):
            return assignment

        # Select an unassigned variable using variable selection heuristics.
        variable = self.csp.choose_next_variable(assignment)

        # Loop through the values in the domain of the selected variable.
        for value in self.csp.order_domain_values(variable):
            # Check if the assignment of the value to the variable is consistent.
            if self.csp.is_consistent(assignment, variable, value):
                # Assign the value to the variable.
                assignment[variable] = value

                # Recursively attempt to complete the assignment.
                result = self.backtrack(assignment)

                # If a solution is found, return it.
                if result:
                    return result

                # If no solution is found, undo the assignment.
                del assignment[variable]

        # If no solution is found, return None to indicate failure.
        return None
