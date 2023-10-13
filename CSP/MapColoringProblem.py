# Map Coloring Problem for CSP input

from CSP import CSP

class MapColoringProblem:

    # constructor
    def __init__(self, countries, colors, adjacency):
        self.variables = countries
        self.constraints = adjacency
        self.domains = {self.variables[i]: colors for i in range(len(self.variables))}

    # return the variables
    def get_variables(self):
        return self.variables
 
    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    def get_domains(self, domains=None, variable=None):
        if variable == None: return self.domains   
        else: return domains[variable]           

    # return the constraints
    def get_constraints(self):
        return self.constraints
    
    # return the neighbors (other variables with a constraint involving) of the current variable 
    def get_neighbors(self, variable): 
        return self.constraints[variable]

    # TODO: add ordering (return variables with more options first)
    # returns the next variable that hasn't been assigned yet (no heuristic)
    def choose_next_variable(self, assignment): 
        #loop through countries
        for country in self.variables: 
            # if the country hasn't been assigned
            if country not in assignment:
                # return it to be visited next
                return country
    
    # TODO: add some ordering 
    # returns a list of domain values for a given variable to search through
    def order_domain_values(self, domains, variable): 
        return domains[variable]

    # returns whether or not the given variable value pair satisfies all constraints with the current assignment 
    def is_consistent(self, assignment, variable, value):
        # for each adjacent country
        for country in self.constraints[variable]: 
            # if that country has the same color as the current assignment
            if country in assignment and assignment[country] == value: return False
        # if none are the same or the country hasn't yet been assigned, return true
        return True



if __name__ == "__main__":
    # setup the australia problem
    australia_countries = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    australia_colors = ["r", "g", "b"]
    australia_adjacency = {"WA": ["NT", "SA"], 
                           "NT":["WA", "SA", "Q"], 
                           "SA":["WA", "NT", "Q", "NSW", "V"], 
                           "Q":["NT", "SA", "NSW"], 
                           "NSW":["Q", "SA", "V"], 
                           "V":["NSW", "SA"], 
                           "T":[]
                           }

    australia_problem = MapColoringProblem(australia_countries, australia_colors, australia_adjacency)

    
    
    # setup the CSPSolver
    australia_csp = CSP(australia_problem)
    
    # test choose_next_variable
    # print(australia_problem.choose_next_variable("WA"))

    # test order_domain_values

    # test the backtracking method
    result = CSP.backtrack(australia_csp)

    print(result)

