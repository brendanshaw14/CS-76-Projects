# Constraint Satisfaction Problem Class

from collections import deque
import copy

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
        - 
    """ 

    # Backtracking Algorithm
    def backtrack(self, domains=None):
        # if this is the first call, set the domains to all possible values
        if domains == None:
            domains = self.csp.domains

        # If the assignment is complete, return it as a solution.
        if self.is_assignment_complete(self.assignment):
            return self.assignment

        # Select an unassigned variable using variable selection heuristics.
        variable = self.csp.choose_next_variable(self.assignment)

        # Loop through the values in the domain of the selected variable.
        for value in self.csp.order_domain_values(variable):

            # Check if the assignment of the value to the variable is consistent.
            if self.csp.is_consistent(self.assignment, variable, value):

                # Assign the value to the variable.
                self.assignment[variable] = value

                # If inference enabled: Recursively attempt to complete the assignment.
                if self.inference:
                    # copy the domain for the recursive calls
                    domain_copy = copy.deepcopy(domains)
                    # call mac3 to edit domain
                    inferences = self.MAC3(domain_copy, variable)
                    # if these are all consistent, keep going
                    if inferences: 
                        result = self.backtrack(self.assignment)

                # If a solution is found, return it.
                if result:
                    return result

            # If no solution is found, undo the assignment.
            del self.assignment[variable]

        # If no solution is found, return None to indicate failure.
        return None

    def MAC3(self, domains, assigned_variable):
        # Initialize a queue for consistency checks
        queue = deque

        # add all of the arcs from the neighbors of the variable to that variable
        for neighbor in self.csp.get_neighbors[assigned_variable]:
            # if the neighbor isn't in the assignment already:
            if neighbor not in self.assignment:
                # add the tuple of the arc from neighbor to variable as a tuple
                queue.append((neighbor, assigned_variable))

        # while there are still items in the queue:
        while queue:
            # get the next variable assignment
            neighbor, assigned_variable = queue.pop()  
            
            # if the neighbor's domain was changed
            if self.revise(self.csp, neighbor, assigned_variable):

                # if the domain is now empty after the change
                if not self.csp.get_domains(neighbor):  # If a domain becomes empty, return failure
                    return False
                
                # otherwise, loop thorugh the neighbors, adding them to the queue to be edited as well
                for neighbor_neighbor in self.csp.get_neighbors(neighbor):
                    # if the neighbor is not assigned (this includes assigned_variable):
                    if neighbor_neighbor not in self.assignment:
                        queue.append((neighbor_neighbor, neighbor))
        return True

    def revise(self, neighbor, variable):
        # starts at false
        revised = False
        # for each value in the domain of the neighbor (D_i)
        for neighbor_value in self.csp.get_domains(neighbor):  

            # for each value in the domain of the variable
            for value in self.csp.get_domains(variable):

                # if that variable doesn't satisfy the constraint
                if not self.csp.is_consistent({neighbor:neighbor_value}, variable, value):
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