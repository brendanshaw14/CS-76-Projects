# Map Coloring Problem for CSP input

from CSP import CSP
import copy

class MapColoringProblem:

    # constructor
    def __init__(self, countries, colors, adjacency, MRV=False):
        self.variables = countries
        self.constraints = adjacency
        self.domains = {self.variables[i]: copy.deepcopy(colors) for i in range(len(self.variables))}

        # minimum remaining values heuristic enable/disable
        self.MRV = MRV

    # return the variables
    def get_variables(self):
        return self.variables
 
    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    def get_domains(self, domains=None, variable=None):
        if variable == None or domains == None: return self.domains   
        else: return domains[variable]           

    
    # return the neighbors (other variables with a constraint involving) of the current variable 
    def get_neighbors(self, variable): 
        return self.constraints[variable]

    # returns the next variable that hasn't been assigned yet (no heuristic)
    def choose_next_variable(self, assignment, domains): 
        # if MRV enabled: 
        if self.MRV:
            # remember the least value and which country: initialize to 4 since there are at most 3 values
            min_remaining_values_country = None
            min_remaining_values = 4
            # loop through the domains
            print(domains)
            for country, remaining_values in domains.items(): 
                # if the country has less values than the current min
                if country not in assignment and len(remaining_values) < min_remaining_values:
                    # udpate the min and country
                    min_remaining_values = len(remaining_values)
                    min_remaining_values_country = country
            return min_remaining_values_country

        # if MRV disabled
        else: 
            # loop through countries
            for country in self.variables: 
                # if the country hasn't been assigned
                if country not in assignment:
                    # return it to be visited next
                    return country
    
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

    australia_problem_nomrv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency)
    australia_problem_mrv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, True)

    
    
    # setup the CSPSolver
    australia_csp_inference = CSP(australia_problem_nomrv, True) 
    australia_csp_no_inference = CSP(australia_problem_nomrv) 
    australia_csp_inference_mrv = CSP(australia_problem_mrv, True) 
    australia_csp_no_inference_mrv = CSP(australia_problem_mrv) 
    
    # test choose_next_variable
    # print(australia_problem.choose_next_variable("WA"))

    # test order_domain_values

    # test the backtracking method
    result = CSP.backtrack(australia_csp_inference_mrv)

    print(result)
# No inference:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# Inference:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# No Inference and MRV:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# Inference and MRV:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
