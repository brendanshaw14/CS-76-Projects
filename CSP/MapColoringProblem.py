# Map Coloring Problem

from CSP import CSP

class MapColoringProblem:

    # constructor
    def __init__(self, countries, colors, adjacency):
        self.countries = countries
        self.colors = colors
        self.adjacency = adjacency
        

    # returns true if all the variables have been assigned
    def is_assignment_complete(self, assignment): 
        # checks if everything in the dictionary is assigned
        for country in assignment:
            if assignment[country] == None: 
                return False
        return True
    
    # TODO: add ordering (return variables with more options first)
    # returns the next variable that hasn't been assigned yet (no heuristic)
    def choose_next_variable(self, assignment): 
        #loop through countries
        for country in self.countries: 
            # if the country hasn't been assigned
            if country not in assignment:
                # return it to be visited next
                return country
    
    # TODO: add ordering (return the valid ones first)
    # returns the domain values to search
    def order_domain_values(self, variable):
        # just return the list of available colors in this case
        return self.colors
        
    def is_consistent(self, variable, value, assignment):
        # for each adjacent country
        for country in self.adjacency[variable]: 
            # if that country has the same color as the current assignment
            if country in assignment and assignment[country] == value: return False
        # if none are the same or the country hasn't yet been assigned, return true
        return True




if __name__ == "__main__":
    # setup the australia problem
    australia_countries = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    australia_colors = ["r", "g", "b"]
    australia_adjacency = {"WA": ["NT", "SA"], "NT":["WA", "SA", "Q"], "SA":["WA", "NT", "Q", "NSW", "V"], "Q":["NT", "SA", "NSW"], "NSW":["Q", "SA", "V"], "V":["NSW", "SA"], "T":[]}
    australia_problem = MapColoringProblem(australia_countries, australia_colors, australia_adjacency)

    # setup the CSPSolver
    australia_csp = CSP(australia_problem)
    result = CSP.backtrack(australia_csp)
    print(result)

