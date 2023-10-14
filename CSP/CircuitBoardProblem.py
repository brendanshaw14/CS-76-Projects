# Circuit BOard Problem for CSP input

from CSP import CSP

class CircuitBoardProblem:

    # constructor
    def __init__(self, components, board_width, board_height):
        self.variables = components
        self.board_width = board_width
        self.board_height = board_height

    # return the problem's variables
    def get_variables(self):
        return self.variables

    #
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
    def choose_next_variable(self, assignment): 
        #loop through components
        for component in self.variables: 
            # if the country hasn't been assigned
            if component not in assignment:
                # return it to be visited next
                return component
    
    # TODO: add ordering (return the valid ones first)
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
    

    # TODO: 
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




if __name__ == "__main__":
    # set up the board's parameters
    components = {"a":(3, 2), "b":(5, 2), "c":(2, 3), "e":(7, 1)}
    board_width = 10
    board_height = 3
    circuit_problem = CircuitBoardProblem(components, board_width, board_height)

    # setup the CSPSolver
    circuit_csp_no_inference = CSP(circuit_problem)
    circuit_csp_inference = CSP(circuit_problem, True)

    # test the order_domain_variables method
    # print(circuit_problem.order_domain_values("c"))
    # test the backtracking method: 
    result = CSP.backtrack(circuit_csp_inference)
    print(result)

#   {'a': (0, 0), 'b': (3, 0), 'c': (8, 0), 'e': (0, 2)}