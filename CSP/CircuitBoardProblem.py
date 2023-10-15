# Circuit BOard Problem for CSP input

from CSP import CSP

class CircuitBoardProblem:

    # constructor- just initializes the boards variables, height, and width
    def __init__(self, components, board_width, board_height, MRV=False):
        self.variables = components
        self.board_width = board_width
        self.board_height = board_height

        # whether or not MRV is enabled
        self.MRV = MRV

    # return the problem's variables
    def get_variables(self):
        return self.variables

    # return all the domains if no variable is specified,
    # otherwise return the domain of that variable
    # TYPE: dictionary if no domain specified, list if specified
    def get_domains(self, domains=None, variable=None): 
        # if no domain or variable specified
        if variable == None or domains == None: 
            domains = {}
            # create a dictionary that has a list of each component's possible locations associated with it 
            for component in self.variables: 
                # add the list of domain values for that component
                domains[component] = self.get_component_domain(component)
            return domains
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
        # if MRV not enabled
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
    circuit_problem_no_mrv = CircuitBoardProblem(components, board_width, board_height)
    circuit_problem_mrv = CircuitBoardProblem(components, board_width, board_height, True)

    # setup the CSPSolver
    circuit_csp_no_inference = CSP(circuit_problem_no_mrv)
    circuit_csp_inference = CSP(circuit_problem_no_mrv, True)
    circuit_csp_no_inference_mrv = CSP(circuit_problem_mrv)
    circuit_csp_inference_mrv = CSP(circuit_problem_mrv, True)

    # test with no inference, no mrv
    # result = CSP.backtrack(circuit_csp_no_inference)
    # print(result)
    # print(circuit_problem_no_mrv.board_to_string(result))

        # {'a': (0, 0), 'b': (3, 0), 'c': (8, 0), 'e': (0, 2)}
        # eeeeeee.cc
        # aaabbbbbcc
        # aaabbbbbcc

    # test with inference, no mrv
    # result = CSP.backtrack(circuit_csp_inference)
    # print(result)
    # print(circuit_problem_no_mrv.board_to_string(result))

        # {'a': (0, 0), 'b': (3, 0), 'c': (8, 0), 'e': (0, 2)}
        # eeeeeee.cc
        # aaabbbbbcc
        # aaabbbbbcc

    # test with no inference, mrv
    # result = CSP.backtrack(circuit_csp_no_inference_mrv)
    # print(result)
    # print(circuit_problem_mrv.board_to_string(result))

        # {'c': (0, 0), 'b': (2, 0), 'e': (2, 2), 'a': (7, 0)}
        # cceeeeeee.
        # ccbbbbbaaa
        # ccbbbbbaaa

    # test with inference, mrv
    # result = CSP.backtrack(circuit_csp_inference_mrv)
    # print(result)
    # print(circuit_problem_mrv.board_to_string(result))

        # {'c': (0, 0), 'a': (2, 0), 'b': (5, 0), 'e': (2, 2)}
        # cceeeeeee.
        # ccaaabbbbb
        # ccaaabbbbb



