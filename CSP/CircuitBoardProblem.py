# Circuit BOard Problem for CSP input

import time
from CSP import CSP

class CircuitBoardProblem:

    # constructor- just initializes the boards variables, height, and width
    def __init__(self, components, board_width, board_height, MRV=False, LCV=False):
        self.variables = components
        self.board_width = board_width
        self.board_height = board_height

        self.MRV = MRV
        self.LCV = LCV

    # return the problem's variables
    def get_variables(self):
        return self.variables

    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    # TYPE: dictionary if no domain specified, list if specified
    def get_domains(self, assignment=None, domains=None, variable=None): 
        # if no domain or variable specified
        if variable == None or domains == None: 
            domains = {}
            # create a dictionary that has a list of each component's possible locations associated with it 
            for component in self.variables: 
                # add the list of domain values for that component
                domains[component] = self.get_component_domain(component)
            return domains
        else: 
            if self.LCV:
                values_with_eliminations = []
                # for each location this variable can take 
                for location in domains[variable]:
                    # remember how many neighboring values it eliminates
                    values_eliminated = 0
                    for neighbor in self.get_neighbors(variable):
                        if location in domains[neighbor]:
                            values_eliminated += 1

                    # Store the color along with the number of eliminated values as a tuple
                    values_with_eliminations.append((location, values_eliminated))

                # Sort the list of tuples based on the second element (values_eliminated) in ascending order
                sorted_values = sorted(values_with_eliminations, key=lambda x: x[1])

                # Extract the sorted colors from the sorted list of tuples
                sorted_components = [component for component, _ in sorted_values]

                # Return the sorted list of colors
                return sorted_components
            else:
                return domains[variable]
    
    # return the neighboring components (this is all of them, since none can overlap)
    def get_neighbors(self, variable): 
        neighbors = []
        # loop through components
        for component in self.variables: 
            # add every one to the list
            neighbors.append(component)
        neighbors.remove(variable)
        return neighbors


    # *****************choose_next_variable*****************"
    #   - returns true if all the variables have been assigned
    #   - chooses the next variable to be used by the CSP solver
    def choose_next_variable(self, assignment, domains): 
        # if MRV enabled: 
        if self.MRV:
            # remember the least value and which component: initialize to the total number of locations on the board
            min_remaining_values_component = None
            min_remaining_values = (self.board_height * self.board_width)
            # loop through the domains
            for component, remaining_values in domains.items(): 
                # if the country has less values than the current min
                if component not in assignment and len(remaining_values) < min_remaining_values:
                    # udpate the min and country
                    min_remaining_values = len(remaining_values)
                    min_remaining_values_component = component
            return min_remaining_values_component
        
        # if no heuristic enabled
        else: 
            # loop through components
            for component in self.variables: 
                # if the country hasn't been assigned
                if component not in assignment:
                    # return it to be visited next
                    return component
    
    # *****************order_domain_values*****************"
    #   - returns the next value in the domain to search
    #   - return the available squares that the component could go into 
    def get_component_domain(self, variable):
        # fetch the height and width of the current component
        component_height = self.variables[variable][1]
        component_width = self.variables[variable][0]

        # save the list of domain values it can take: 
        domain_values = []

        # for each x up to the board's width - the component's width
        for x in range(0, self.board_width-component_width+1):
            # for each y starting from the height of the board up to the board's height
            for y in range(0, self.board_height-component_height+1):
                # add that value tuple to the list
                domain_values.append((x, y))
        # Return the list
        return domain_values
    

    # ******************is_consistent******************
    #   -returns whether or not giving the input variable the input 
    #   value is within the constraints of the problem. 
    #   - return whether or not the rectangle assginment overlaps with any other rectangles
    def is_consistent(self, assignment, variable, value):
        # get the x, y, width, and height of the new rectangle
        new_x, new_y = value  # Bottom-left coordinates of the new component
        new_width, new_height = self.variables[variable]  # Width and height of the new component

        # loop through the existing rectangles in the assignment
        for component in assignment: 
            # get the x, y, width, and height of that new component
            existing_x, existing_y = assignment[component]  # Bottom-left coordinates of existing component
            existing_width, existing_height = self.variables[component]  # Width and height of existing component

            # Check for overlap along the x-axis
            if (new_x < existing_x + existing_width) and (existing_x < new_x + new_width):
                # Check for overlap along the y-axis
                if (new_y < existing_y + existing_height) and (existing_y < new_y + new_height):
                    # Rectangles overlap
                    return False  # Overlap detected

        # No overlap
        return True  # No overlap detected

    # takes an input dictionary that assigns component variable keys to tuple location values and prints them out
    # TYPE: string
    def board_to_string(self, assignment):
        board = [['.' for _ in range(self.board_width)] for _ in range(self.board_height)]

        for component, position in assignment.items():
            x, y = position
            component_width, component_height = self.variables[component]

            for i in range(y, y + component_height):
                for j in range(x, x + component_width):
                    board[i][j] = component
                    
        return '\n'.join([''.join(row) for row in reversed(board)])
        




if __name__ == "__main__":
    # set up the board's parameters
    components = {"a":(3, 2), "b":(5, 2), "c":(2, 3), "e":(7, 1)}
    board_width = 10
    board_height = 3

    circuit_problem_no_heuristic = CircuitBoardProblem(components, board_width, board_height)
    circuit_problem_mrv = CircuitBoardProblem(components, board_width, board_height, MRV=True)
    circuit_problem_lcv = CircuitBoardProblem(components, board_width, board_height, LCV=True)
    circuit_problem_mrv_lcv = CircuitBoardProblem(components, board_width, board_height, MRV=True, LCV=True)

    # setup the CSPSolver without inference
    circuit_csp_no_inference_no_heuristic = CSP(circuit_problem_no_heuristic)
    circuit_csp_no_inference_mrv = CSP(circuit_problem_mrv)
    circuit_csp_no_inference_lcv = CSP(circuit_problem_lcv)
    circuit_csp_no_inference_mrv_lcv = CSP(circuit_problem_mrv_lcv)

    # setup the CSPSolver with inference
    circuit_csp_inference_no_heuristic = CSP(circuit_problem_mrv, True)
    circuit_csp_inference_mrv = CSP(circuit_problem_mrv, True)
    circuit_csp_inference_lcv = CSP(circuit_problem_lcv, True)
    circuit_csp_inference_mrv_lcv = CSP(circuit_problem_mrv_lcv, True)

    # test no inference no heuristics 
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_no_inference_no_heuristic)
    end_time = time.time()
    print(f"No Inference No Heuristics Runtime: {end_time - start_time} seconds")
    print(circuit_problem_no_heuristic.board_to_string(result)) 

    # test no inference MRV 
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_no_inference_mrv)
    end_time = time.time()
    print(f"No Inference MRV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_mrv.board_to_string(result)) 

    # test no inference LCV 
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_no_inference_lcv)
    end_time = time.time()
    print(f"No Inference LCV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_lcv.board_to_string(result))

    # test no inference MRV and LCV 
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_no_inference_mrv_lcv)
    end_time = time.time()
    print(f"No Inference MRV LCV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_mrv_lcv.board_to_string(result))

    # test inference no heuristic
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_inference_no_heuristic)
    end_time = time.time()
    print(f"Inference No Heuristic Runtime: {end_time - start_time} seconds")
    print(circuit_problem_no_heuristic.board_to_string(result))

    # test inference MRV
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_inference_mrv)
    end_time = time.time()
    print(f"Inference MRV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_mrv.board_to_string(result))

    # test inference LCV
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_inference_lcv)
    end_time = time.time()
    print(f"Inference LCV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_lcv.board_to_string(result))

    # test inference MRV LCV
    start_time = time.time()
    result = CSP.backtrack(circuit_csp_inference_mrv_lcv)
    end_time = time.time()
    print(f"Inference MRV LCV Runtime: {end_time - start_time} seconds")
    print(circuit_problem_mrv_lcv.board_to_string(result))













