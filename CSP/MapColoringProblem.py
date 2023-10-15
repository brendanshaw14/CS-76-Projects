# Map Coloring Problem for CSP input

from CSP import CSP
import copy
import time 

class MapColoringProblem:

    # constructor
    def __init__(self, countries, colors, adjacency, MRV=False, DEG=False, LCV=False):
        self.variables = countries
        self.constraints = adjacency
        self.domains = {self.variables[i]: copy.deepcopy(colors) for i in range(len(self.variables))}

        # minimum remaining values heuristic enable/disable
        self.MRV = MRV
        self.DEG = DEG
        self.LCV = LCV

    # return the variables
    def get_variables(self):
        return self.variables
 
    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    def get_domains(self, assignment=None, domains=None, variable=None):
        # if this is the initial call, return the entire domains dict
        if variable == None or domains == None: 
            return self.domains   

        # if we are getting the domain of a specific variable
        else: 
            # if LCV heuristic is enabled
            if self.LCV:
                values_with_eliminations = []

                for color in domains[variable]:
                    values_eliminated = 0
                    for neighbor in self.get_neighbors(variable):
                        if color in domains[neighbor]:
                            values_eliminated += 1

                    # Store the color along with the number of eliminated values as a tuple
                    values_with_eliminations.append((color, values_eliminated))

                # Sort the list of tuples based on the second element (values_eliminated) in ascending order
                sorted_values = sorted(values_with_eliminations, key=lambda x: x[1])

                # Extract the sorted colors from the sorted list of tuples
                sorted_colors = [color for color, _ in sorted_values]

                # Return the sorted list of colors
                return sorted_colors

            else:
                return domains[variable]           

    
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
            for country, remaining_values in domains.items(): 
                # if the country has less values than the current min

                if country not in assignment and len(remaining_values) < min_remaining_values:
                    # udpate the min and country
                    min_remaining_values = len(remaining_values)
                    min_remaining_values_country = country

            return min_remaining_values_country

        # if degree heuristic is enabled
        elif self.DEG:
            # return the variable involved with the most other variables (highest adjacency list size)
            highest_deg_country = None
            highest_deg = -1 # initialize to -1 so this will be updated for sure
            # loop through the adjacency list
            for country, adjacency_list in self.constraints.items(): 
                # if the country has a higher degree than the current
                if country not in assignment and len(adjacency_list) > highest_deg: 
                    highest_deg = len(adjacency_list)
                    highest_deg_country = country
            return highest_deg_country

        # if no heuristic enabled
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
    # initialize the different problem classes
    australia_problem_no_heuristic = MapColoringProblem(australia_countries, australia_colors, australia_adjacency)
    australia_problem_mrv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, MRV=True)
    australia_problem_deg = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, DEG=True)
    australia_problem_lcv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, LCV=True)
    australia_problem_mrv_lcv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, MRV=True, LCV=True)
    australia_problem_deg_lcv = MapColoringProblem(australia_countries, australia_colors, australia_adjacency, DEG=True, LCV=True)

    # setup the CSPSolver problems without inference
    australia_csp_no_inference_no_heuristic = CSP(australia_problem_no_heuristic) 
    australia_csp_no_inference_mrv = CSP(australia_problem_mrv) 
    australia_csp_no_inference_deg = CSP(australia_problem_deg) 
    australia_csp_no_inference_lcv = CSP(australia_problem_lcv) 
    australia_csp_no_inference_mrv_lcv = CSP(australia_problem_mrv_lcv) 
    australia_csp_no_inference_deg_lcv = CSP(australia_problem_deg_lcv) 

    # With inference
    australia_csp_inference_no_heuristic = CSP(australia_problem_no_heuristic, True) 
    australia_csp_inference_mrv = CSP(australia_problem_mrv, True) 
    australia_csp_inference_deg = CSP(australia_problem_deg, True) 
    australia_csp_inference_lcv = CSP(australia_problem_lcv, True) 
    australia_csp_inference_mrv_lcv = CSP(australia_problem_mrv_lcv, True) 
    australia_csp_inference_deg_lcv = CSP(australia_problem_deg_lcv, True) 

    # test no inference no heuristics 
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_no_heuristic)
    end_time = time.time()
    print(f"No Inference No Heuristics Runtime: {end_time - start_time} seconds")
    print(result)

    # test no inference with MRV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_mrv)
    end_time = time.time()
    print(f"No Inference with MRV Runtime: {end_time - start_time} seconds")
    print(result)

    # test no inference with DEG
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_deg)
    end_time = time.time()
    print(f"No Inference with DEG Runtime: {end_time - start_time} seconds")
    print(result)

    # test no inference with LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_lcv)
    end_time = time.time()
    print(f"No Inference with LCV Runtime: {end_time - start_time} seconds")
    print(result)

    # test no inference with MRV and LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_mrv_lcv)
    end_time = time.time()
    print(f"No Inference with MRV and LCV Runtime: {end_time - start_time} seconds")
    print(result)

    # test no inference with DEG and LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_no_inference_deg_lcv)
    end_time = time.time()
    print(f"No Inference with DEG and LCV Runtime: {end_time - start_time} seconds")
    print(result)

    # test inference with no heuristic
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_no_heuristic)
    end_time = time.time()
    print(f"Inference with No Heuristics Runtime: {end_time - start_time} seconds")
    print(result)


    # test inference with MRV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_mrv)
    end_time = time.time()
    print(f"Inference with MRV Runtime: {end_time - start_time} seconds")
    print(result)

    # test inference with DEG
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_deg)
    end_time = time.time()
    print(f"Inference with DEG Runtime: {end_time - start_time} seconds")
    print(result)

    # test inference with LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_lcv)
    end_time = time.time()
    print(f"Inference with LCV Runtime: {end_time - start_time} seconds")
    print(result)

    # test inference with MRV and LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_mrv_lcv)
    end_time = time.time()
    print(f"Inference with MRV and LCV Runtime: {end_time - start_time} seconds")
    print(result)

    # test inference with DEG and LCV
    start_time = time.time()
    result = CSP.backtrack(australia_csp_inference_deg_lcv)
    end_time = time.time()
    print(f"Inference with DEG and LCV Runtime: {end_time - start_time} seconds")
    print(result)
    







# No inference:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# Inference:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# No Inference and MRV:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
# Inference and MRV:
#    {'WA': 'r', 'NT': 'g', 'SA': 'b', 'Q': 'r', 'NSW': 'g', 'V': 'r', 'T': 'r'}
