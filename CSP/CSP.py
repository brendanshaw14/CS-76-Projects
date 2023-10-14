# Constraint Satisfaction Problem Class

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
            domains = self.csp.get_domains()
        

        # If the assignment is complete, return it as a solution.
        if self.is_assignment_complete(self.assignment):
            return self.assignment

        # Select an unassigned variable using variable selection heuristics.
        variable = self.csp.choose_next_variable(self.assignment)
        print("Calling backtrack on " + str(variable))

        # Loop through the values in the domain of the selected variable
        for value in self.csp.order_domain_values(domains, variable):
            print("Testing value " + str(value))
            # Check if the assignment of the value to the variable is consistent with the rest of the assignment.
            if self.csp.is_consistent(self.assignment, variable, value):

                # Assign the value to the variable.
                self.assignment[variable] = value

                # If inference enabled: Recursively attempt to complete the assignment.
                if self.inference:
                    # copy the domain for the recursive calls
                    domains_copy = copy.deepcopy(domains)
                    # edit the domain of the assigned variable
                    domains_copy[variable] = [value]
                    print("Domain copy: " + str(domains_copy))
                    # call mac3 to edit domain
                    inferences = self.MAC3(domains_copy, variable)
                    # if these are all consistent, keep going
                    if inferences: 
                        print("inferences true")
                        result = self.backtrack(self.assignment, domains_copy)
                    else: 
                        result = None
                # if inference isn't enabled, call backtrack recursively again with the same domain
                else:
                    result = self.backtrack(domains)

                # If a solution is found, return it.
                if result:
                    return result

                # If no solution is found, undo the assignment.
                del self.assignment[variable]

        # If no solution is found, return None to indicate failure.
        return None

    def MAC3(self, domains, assigned_variable):
        # Initialize a queue for consistency checks
        queue = []

        # add all of the arcs from the neighbors of the variable to that variable
        for neighbor in self.csp.get_neighbors(assigned_variable):
            # if the neighbor isn't in the assignment already:
            if neighbor not in self.assignment:
                # add the tuple of the arc from neighbor to variable as a tuple
                queue.append((neighbor, assigned_variable))

        print("queue: " + str(queue))
        # while there are still items in the queue:
        while queue:
            # get the next variable assignment
            neighbor, assigned_variable = queue.pop()  
            
            # if the neighbor's domain was changed
            if self.revise(domains, neighbor, assigned_variable):

                # if the domain is now empty after the change
                if not self.csp.get_domains(domains, neighbor):  # If a domain becomes empty, return failure
                    return False
                
                # otherwise, loop thorugh the neighbors, adding them to the queue to be edited as well
                for neighbor_neighbor in self.csp.get_neighbors(neighbor):
                    # if the neighbor is not assigned (this includes assigned_variable):
                    if neighbor_neighbor not in self.assignment:
                        queue.append((neighbor_neighbor, neighbor))
        return True

    def revise(self, domains, neighbor, assigned_variable):
        # starts at false
        revised = False
        print("Calling revise on " + str(neighbor) + ", " + str(assigned_variable))
        # for each value in the domain of the neighbor (D_i)
        for neighbor_value in self.csp.get_domains(domains, neighbor):  
            # for each value in the domain of the variable
            print("Here")
            for value in self.csp.get_domains(domains, assigned_variable):
                print("Testing consistency of " + str(value) + " for variable " + str(assigned_variable) + " with assignment " + str({neighbor:neighbor_value}))

                # if that variable doesn't satisfy the constraint
                if not self.csp.is_consistent({neighbor:neighbor_value}, assigned_variable, value):
                    print(domains[neighbor])
                    domains[neighbor].remove(neighbor_value)  # Remove inconsistent values from the domain
                    print("removing value " + str(neighbor_value) + " from the domain of " + str(neighbor))
                    print(domains[neighbor])
                    print("revised domains " + str(domains))
                    revised = True
                    break
        return revised

    # returns true if all the variables have been assigned
    def is_assignment_complete(self, assignment): 
        # if the length of the assignment is the same as the number of countries
        if len(assignment) == len(self.csp.get_variables()): 
            return True
        return False