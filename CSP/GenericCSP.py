# Map Coloring Problem for CSP input

from CSP import CSP
import copy
class GenericCSP:

    # constructor
    def __init__(self, variables, domain_values, constraints):
        self.variables = variables # list of variables
        self.constraints = constraints # adjacency dictionary: which items are constrianed with one another
        self.domains = {self.variables[i]: copy.deepcopy(domain_values) for i in range(len(self.variables))} # dictionary of each variable and its possible domain values

    # return the problems variables
    # TYPE: list
    def get_variables(self):
        return self.variables
 
    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    # TYPE: dictionary if no domain specified, list if specified
    def get_domains(self, domains=None, variable=None):
        if variable == None or domains == None: return self.domains   
        else: return domains[variable]           

    
    # return the neighbors (other variables with a constraint involving) of the current variable 
    # TYPE: list
    def get_neighbors(self, variable): 
        return self.constraints[variable]

    # returns the next variable that hasn't been assigned yet (no heuristic)
    # TYPE: identical to the problem's variable type
    def choose_next_variable(self, assignment): 
        #loop through countries
        for variable in self.variables: 
            # if the country hasn't been assigned
            if variable not in assignment:
                # return it to be visited next
                return variable
    
    # returns whether or not the given variable value pair satisfies all constraints with the current assignment 
    # if only one item is given in the assignment, it will check for that one item only
    # TYPE: boolean
    def is_consistent(self, assignment, variable, value):
        # implememt assignment consistency here



if __name__ == "__main__":
    pass