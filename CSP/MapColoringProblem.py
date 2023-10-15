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
        self.colors = colors
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
            # remember the least value and which country: initialize to num_colors + 1
            min_remaining_values_country = None
            min_remaining_values = len(self.colors) + 1

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
    australia_adjacency = {
        "WA": ["NT", "SA"], 
        "NT":["WA", "SA", "Q"], 
        "SA":["WA", "NT", "Q", "NSW", "V"], 
        "Q":["NT", "SA", "NSW"], 
        "NSW":["Q", "SA", "V"], 
        "V":["NSW", "SA"], 
        "T":[]
    }

    # uncomment these to switch to the US coloring problem. 
    # names are still australia so that all of the same testing code can be used. 
    # australia_colors = ["r", "g", "b", "y"]
    # australia_countries = [
        # "WA", "OR", "ID", "CA", "NV", "MT", "WY", "UT", "AZ", "NM",
        # "CO", "ND", "SD", "NE", "KS", "OK", "TX", "MN", "IA", "MO",
        # "AR", "LA", "WI", "IL", "MI", "IN", "OH", "KY", "WV", "PA",
        # "NY", "VT", "NH", "ME", "MA", "CT", "RI", "NJ", "DE", "MD",
        # "VA", "NC", "SC", "GA", "FL", "AL", "MS", "TN", "HI", "AK"
    # ]
    # australia_adjacency = {
        # "WA": ["OR", "ID"],
        # "OR": ["WA", "ID", "CA", "NV"],
        # "ID": ["WA", "MT", "WY", "UT", "NV", "OR"],
        # "CA": ["OR", "NV", "AZ"],
        # "NV": ["OR", "ID", "UT", "AZ", "CA"],
        # "MT": ["ID", "ND", "SD", "WY"],
        # "WY": ["ID", "MT", "SD", "NE", "CO", "UT"],
        # "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
        # "AZ": ["CA", "NV", "UT", "NM"],
        # "NM": ["AZ", "UT", "CO", "OK", "TX"],
        # "CO": ["WY", "NE", "KS", "OK", "NM", "UT"],
        # "ND": ["MT", "MN", "SD"],
        # "SD": ["ND", "MT", "WY", "NE", "IA", "MN"],
        # "NE": ["SD", "WY", "CO", "KS", "MO", "IA"],
        # "KS": ["NE", "CO", "OK", "MO"],
        # "OK": ["KS", "CO", "NM", "TX", "AR", "MO"],
        # "TX": ["OK", "NM", "AR", "LA"],
        # "MN": ["ND", "SD", "IA", "WI"],
        # "IA": ["MN", "SD", "NE", "MO", "IL", "WI"],
        # "MO": ["IA", "NE", "KS", "OK", "AR", "TN", "KY", "IL"],
        # "AR": ["MO", "OK", "TX", "LA", "MS", "TN"],
        # "LA": ["TX", "AR", "MS"],
        # "WI": ["MN", "IA", "IL", "MI"],
        # "IL": ["WI", "IA", "MO", "KY", "IN", "MI"],
        # "MI": ["WI", "IL", "IN", "OH"],
        # "IN": ["MI", "IL", "KY", "OH"],
        # "OH": ["MI", "IN", "KY", "WV", "PA"],
        # "KY": ["OH", "IN", "IL", "MO", "TN", "WV"],
        # "WV": ["PA", "OH", "KY", "VA", "MD"],
        # "PA": ["OH", "WV", "MD", "DE", "NJ", "NY"],
        # "NY": ["PA", "NJ", "VT", "MA", "CT"],
        # "VT": ["NY", "NH"],
        # "NH": ["VT", "ME"],
        # "ME": ["NH"],
        # "MA": ["NY", "CT", "RI"],
        # "CT": ["MA", "RI", "NY"],
        # "RI": ["MA", "CT"],
        # "NJ": ["NY", "PA", "DE"],
        # "DE": ["NJ", "MD", "PA"],
        # "MD": ["DE", "PA", "WV", "VA"],
        # "VA": ["MD", "WV", "KY", "NC", "TN"],
        # "NC": ["VA", "TN", "GA", "SC"],
        # "SC": ["NC", "GA"],
        # "GA": ["NC", "SC", "FL", "AL", "TN"],
        # "FL": ["GA", "AL"],
        # "AL": ["FL", "GA", "MS", "TN"],
        # "MS": ["AL", "LA", "AR", "TN"],
        # "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO", "IL", "KY"],
        # "HI": [],
        # "AK": []
    # }

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
    


# Here are the results of the above tests on the states problem: I'll spare the time
"""
No Inference No Heuristics Runtime: 16.84667181968689 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'r', 'NV': 'y', 'MT': 'r', 'WY': 'g', 'UT': 'r', 'AZ': 'g', 'NM': 'b', 'CO': 'y', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'r', 'TX': 'g', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'y', 'LA': 'r', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'y', 'WV': 'g', 'PA': 'b', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'g', 'DE': 'r', 'MD': 'y', 'VA': 'r', 'NC': 'b', 'SC': 'r', 'GA': 'y', 'FL': 'g', 'AL': 'r', 'MS': 'b', 'TN': 'g', 'HI': 'r', 'AK': 'r'}
No Inference with MRV Runtime: 21.745162963867188 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'r', 'NV': 'y', 'MT': 'r', 'WY': 'g', 'UT': 'r', 'AZ': 'g', 'NM': 'b', 'CO': 'y', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'r', 'TX': 'g', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'y', 'LA': 'r', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'y', 'WV': 'g', 'PA': 'b', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'g', 'DE': 'r', 'MD': 'y', 'VA': 'r', 'NC': 'b', 'SC': 'r', 'GA': 'y', 'FL': 'g', 'AL': 'r', 'MS': 'b', 'TN': 'g', 'HI': 'r', 'AK': 'r'}
No Inference with DEG Runtime: 0.00015997886657714844 seconds
{'TN': 'r', 'MO': 'g', 'ID': 'r', 'WY': 'g', 'UT': 'b', 'CO': 'r', 'SD': 'r', 'NE': 'b', 'OK': 'b', 'IA': 'y', 'AR': 'y', 'IL': 'r', 'KY': 'b', 'PA': 'r', 'NV': 'g', 'NM': 'g', 'OH': 'g', 'WV': 'y', 'NY': 'g', 'VA': 'g', 'GA': 'g', 'OR': 'b', 'MT': 'b', 'AZ': 'r', 'KS': 'y', 'TX': 'r', 'MN': 'b', 'WI': 'g', 'MI': 'b', 'IN': 'y', 'MD': 'b', 'NC': 'b', 'AL': 'b', 'MS': 'g', 'CA': 'y', 'ND': 'g', 'LA': 'b', 'MA': 'r', 'CT': 'b', 'NJ': 'b', 'DE': 'g', 'WA': 'g', 'VT': 'r', 'NH': 'g', 'RI': 'g', 'SC': 'r', 'FL': 'r', 'ME': 'r', 'HI': 'r', 'AK': 'r'}
No Inference with LCV Runtime: 34.742955923080444 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'r', 'NV': 'y', 'MT': 'r', 'WY': 'g', 'UT': 'r', 'AZ': 'g', 'NM': 'b', 'CO': 'y', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'r', 'TX': 'g', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'y', 'LA': 'r', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'y', 'WV': 'g', 'PA': 'b', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'g', 'DE': 'r', 'MD': 'y', 'VA': 'r', 'NC': 'b', 'SC': 'r', 'GA': 'y', 'FL': 'g', 'AL': 'r', 'MS': 'b', 'TN': 'g', 'HI': 'r', 'AK': 'r'}
No Inference with MRV and LCV Runtime: 39.77112007141113 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'r', 'NV': 'y', 'MT': 'r', 'WY': 'g', 'UT': 'r', 'AZ': 'g', 'NM': 'b', 'CO': 'y', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'r', 'TX': 'g', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'y', 'LA': 'r', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'y', 'WV': 'g', 'PA': 'b', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'g', 'DE': 'r', 'MD': 'y', 'VA': 'r', 'NC': 'b', 'SC': 'r', 'GA': 'y', 'FL': 'g', 'AL': 'r', 'MS': 'b', 'TN': 'g', 'HI': 'r', 'AK': 'r'}
No Inference with DEG and LCV Runtime: 0.00026297569274902344 seconds
{'TN': 'r', 'MO': 'g', 'ID': 'r', 'WY': 'g', 'UT': 'b', 'CO': 'r', 'SD': 'r', 'NE': 'b', 'OK': 'b', 'IA': 'y', 'AR': 'y', 'IL': 'r', 'KY': 'b', 'PA': 'r', 'NV': 'g', 'NM': 'g', 'OH': 'g', 'WV': 'y', 'NY': 'g', 'VA': 'g', 'GA': 'g', 'OR': 'b', 'MT': 'b', 'AZ': 'r', 'KS': 'y', 'TX': 'r', 'MN': 'b', 'WI': 'g', 'MI': 'b', 'IN': 'y', 'MD': 'b', 'NC': 'b', 'AL': 'b', 'MS': 'g', 'CA': 'y', 'ND': 'g', 'LA': 'b', 'MA': 'r', 'CT': 'b', 'NJ': 'b', 'DE': 'g', 'WA': 'g', 'VT': 'r', 'NH': 'g', 'RI': 'g', 'SC': 'r', 'FL': 'r', 'ME': 'r', 'HI': 'r', 'AK': 'r'}
Inference with No Heuristics Runtime: 86.06060576438904 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'r', 'NV': 'y', 'MT': 'r', 'WY': 'g', 'UT': 'r', 'AZ': 'g', 'NM': 'b', 'CO': 'y', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'r', 'TX': 'g', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'y', 'LA': 'r', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'y', 'WV': 'g', 'PA': 'b', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'g', 'DE': 'r', 'MD': 'y', 'VA': 'r', 'NC': 'b', 'SC': 'r', 'GA': 'y', 'FL': 'g', 'AL': 'r', 'MS': 'b', 'TN': 'g', 'HI': 'r', 'AK': 'r'}
Inference with MRV Runtime: 0.005126953125 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'NV': 'r', 'CA': 'b', 'UT': 'g', 'AZ': 'y', 'WY': 'r', 'MT': 'g', 'NM': 'r', 'CO': 'b', 'SD': 'b', 'ND': 'r', 'NE': 'g', 'KS': 'r', 'OK': 'g', 'TX': 'b', 'MN': 'g', 'IA': 'r', 'MO': 'b', 'AR': 'r', 'LA': 'g', 'WI': 'b', 'IL': 'g', 'MI': 'r', 'IN': 'b', 'OH': 'g', 'KY': 'r', 'WV': 'b', 'PA': 'r', 'MD': 'y', 'DE': 'g', 'NJ': 'b', 'NY': 'g', 'VA': 'g', 'MS': 'b', 'TN': 'y', 'NC': 'r', 'GA': 'g', 'AL': 'r', 'SC': 'b', 'FL': 'b', 'VT': 'r', 'NH': 'g', 'ME': 'r', 'MA': 'r', 'CT': 'b', 'RI': 'g', 'HI': 'r', 'AK': 'r'}
Inference with DEG Runtime: 0.0032498836517333984 seconds
{'TN': 'r', 'MO': 'g', 'ID': 'r', 'WY': 'g', 'UT': 'b', 'CO': 'r', 'SD': 'r', 'NE': 'b', 'OK': 'b', 'IA': 'y', 'AR': 'y', 'IL': 'b', 'KY': 'y', 'PA': 'r', 'NV': 'g', 'NM': 'g', 'OH': 'g', 'WV': 'b', 'NY': 'g', 'VA': 'g', 'GA': 'g', 'OR': 'b', 'MT': 'b', 'AZ': 'r', 'KS': 'y', 'TX': 'r', 'MN': 'g', 'WI': 'r', 'MI': 'y', 'IN': 'r', 'MD': 'y', 'NC': 'b', 'AL': 'b', 'MS': 'g', 'CA': 'y', 'ND': 'y', 'LA': 'b', 'MA': 'r', 'CT': 'b', 'NJ': 'b', 'DE': 'g', 'WA': 'g', 'VT': 'r', 'NH': 'g', 'RI': 'g', 'SC': 'r', 'FL': 'r', 'ME': 'r', 'HI': 'r', 'AK': 'r'}
Inference with LCV Runtime: 0.0055332183837890625 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'CA': 'b', 'NV': 'r', 'MT': 'r', 'WY': 'g', 'UT': 'y', 'AZ': 'g', 'NM': 'r', 'CO': 'b', 'ND': 'g', 'SD': 'b', 'NE': 'r', 'KS': 'g', 'OK': 'y', 'TX': 'b', 'MN': 'r', 'IA': 'g', 'MO': 'b', 'AR': 'r', 'LA': 'g', 'WI': 'b', 'IL': 'r', 'MI': 'g', 'IN': 'b', 'OH': 'r', 'KY': 'g', 'WV': 'y', 'PA': 'g', 'NY': 'r', 'VT': 'g', 'NH': 'r', 'ME': 'g', 'MA': 'g', 'CT': 'b', 'RI': 'r', 'NJ': 'b', 'DE': 'y', 'MD': 'r', 'VA': 'b', 'NC': 'r', 'SC': 'y', 'GA': 'b', 'FL': 'y', 'AL': 'r', 'MS': 'b', 'TN': 'y', 'HI': 'r', 'AK': 'r'}
Inference with MRV and LCV Runtime: 0.008306026458740234 seconds
{'WA': 'r', 'OR': 'g', 'ID': 'b', 'NV': 'r', 'CA': 'b', 'UT': 'g', 'AZ': 'y', 'WY': 'r', 'MT': 'g', 'NM': 'r', 'CO': 'b', 'SD': 'b', 'ND': 'r', 'NE': 'g', 'KS': 'r', 'OK': 'g', 'TX': 'b', 'MN': 'g', 'IA': 'r', 'MO': 'b', 'AR': 'r', 'LA': 'g', 'WI': 'b', 'IL': 'g', 'MI': 'r', 'IN': 'b', 'OH': 'g', 'KY': 'r', 'WV': 'b', 'PA': 'r', 'MD': 'y', 'DE': 'g', 'NJ': 'b', 'NY': 'g', 'VA': 'g', 'MS': 'b', 'TN': 'y', 'NC': 'r', 'GA': 'b', 'SC': 'g', 'AL': 'r', 'FL': 'g', 'VT': 'r', 'NH': 'g', 'ME': 'r', 'MA': 'r', 'CT': 'b', 'RI': 'g', 'HI': 'r', 'AK': 'r'}
Inference with DEG and LCV Runtime: 0.004997968673706055 seconds
{'TN': 'r', 'MO': 'g', 'ID': 'r', 'WY': 'g', 'UT': 'b', 'CO': 'r', 'SD': 'r', 'NE': 'b', 'OK': 'b', 'IA': 'y', 'AR': 'y', 'IL': 'b', 'KY': 'y', 'PA': 'y', 'NV': 'g', 'NM': 'g', 'OH': 'b', 'WV': 'r', 'NY': 'r', 'VA': 'g', 'GA': 'g', 'OR': 'b', 'MT': 'b', 'AZ': 'r', 'KS': 'y', 'TX': 'r', 'MN': 'b', 'WI': 'r', 'MI': 'y', 'IN': 'r', 'MD': 'b', 'NC': 'b', 'AL': 'y', 'MS': 'g', 'CA': 'y', 'ND': 'g', 'LA': 'b', 'MA': 'g', 'CT': 'b', 'NJ': 'b', 'DE': 'r', 'WA': 'g', 'VT': 'g', 'NH': 'r', 'RI': 'r', 'SC': 'r', 'FL': 'r', 'ME': 'g', 'HI': 'r', 'AK': 'r'}
"""



