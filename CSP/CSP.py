# Constraint Satisfaction Problem Class

from collections import deque

class CSP:
    # constructor
    def __init__(self, csp, inference=False):
        self.csp = csp
        self.assignment = {}
        self.inference = inference

    """
    notes: 
        - make a copy of the domains to pass to inference so that it doesn't change the domains when recursion stops 
        - use a method to get neighbors and pass it the domains list 
    """ 

    # Backtracking Algorithm
    def backtrack(self):
        print("Calling backtrack: "+ str(self.assignment))
        # If the assignment is complete, return it as a solution.
        if self.is_assignment_complete(self.assignment):
            return self.assignment

        # Select an unassigned variable using variable selection heuristics.
        variable = self.csp.choose_next_variable(self.assignment)
        print("Next variable:" + str(variable))

        # Loop through the values in the domain of the selected variable.
        for value in self.csp.order_domain_values(variable):
            print(str(variable) + " domain value " + str(value))
            # Check if the assignment of the value to the variable is consistent.
            if self.csp.is_consistent(self.assignment, variable, value):
                # Assign the value to the variable.
                self.assignment[variable] = value

                # If inference enabled: Recursively attempt to complete the assignment.
                if self.inference:
                    inferences = self.MAC3(variable)
                    if inferences: 
                        result = self.backtrack(self.assignment)

                # If a solution is found, return it.
                if result:
                    return result

            # If no solution is found, undo the assignment.
            del self.assignment[variable]

        # If no solution is found, return None to indicate failure.
        return None

    def MAC3(self, variable):
        # Initialize a queue for consistency checks
        queue = deque

        # add all of the arcs from the neighbors of the variable to that variable
        for neighbor in self.csp.get_constraints[variable]:
            if neighbor in self.assignment:
                queue.append((neighbor, variable))

        # while there are still items in the queue:
        while queue:
            # get the next variable-value assignment
            neighbor, variable = queue.pop(0)  # Get the next variable-value pair
            if self.revise(self.csp, variable, value):
                if not self.csp.get_domains(variable):  # If a domain becomes empty, return failure
                    return False
                for neighbor in self.csp.get_neighbors(variable):
                    if neighbor != variable:
                        for neighbor_value in self.csp.get_domains(neighbor):
                            queue.append((neighbor, neighbor_value))
        return True

    def revise(self, variable, value):
        revised = False
        # for each variable related to the current variable:
        for neighbor in self.csp.get_constraints(variable):  
            # for each possible value its neighbor could take:
            for neighbor_value in self.csp.get_domains(constraint):
                
                if not self.csp.is_consistent(variable, value, constraint, neighbor_value):
                    self.csp.remove_value(variable, value)  # Remove inconsistent values from the domain
                    revised = True
                    break
        return revised

    # returns true if all the variables have been assigned
    def is_assignment_complete(self, assignment): 
        # if the length of the assignment is the same as the number of countries
        if len(assignment) == len(self.csp.variables): 
            return True
        return False