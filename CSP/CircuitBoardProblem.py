# Circuit BOard Problem for CSP input

from CSP import CSP

class CircuitBoardProblem:

    # constructor
    def __init__(self, components, board_width, board_height):
        self.components = components
        self.board_width = board_width
        self.board_height = board_height

    # TODO: 
    # *****************is_assignment_complete*****************"
    #   -returns whether or not the assignment is the same lenght
    #    as thenumber of variables, ensuring that every variable has an assignment
    # returns true if all the variables have been assigned
    def is_assignment_complete(self, assignment): 
        # if the length of the assignment is the same as the number of countries
        if len(assignment) == len(self.components): 
            return True
        return False

    # *****************choose_next_variable*****************"
    #   - returns true if all the variables have been assigned
    #   - chooses the next variable to be used by the CSP solver
    def choose_next_variable(self, assignment): 
        #loop through components
        for component in self.components: 
            # if the country hasn't been assigned
            if component not in assignment:
                # return it to be visited next
                return component
    
    # TODO: add ordering (return the valid ones first)
    # *****************order_domain_values*****************"
    #   - returns the next value in the domain to search
    #   - return the available squares that the component could go into 
    def order_domain_values(self, variable):
        # fetch the height and width of the current component
        component_height = self.components[variable][1]
        component_width = self.components[variable][0]

        # save the list of domain values it can take: 
        domain_values = []

        # for each x up to the board's width - the component's width
        for x in range(0, self.board_width-component_width+1):
            # for each y starting from the height of the board up to the board's height
            for y in range(0, self.board_height-component_height+1):
                print(x, y)
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
        new_width, new_height = self.components[variable]  # Width and height of the new component

        # loop through the existing rectangles in the assignment
        for component in assignment: 
            # get the x, y, width, and height of that new component
            existing_x, existing_y = assignment[component]  # Bottom-left coordinates of existing component
            existing_width, existing_height = self.components[component]  # Width and height of existing component

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
    circuit_csp = CSP(circuit_problem)

    # test the order_domain_variables method
    # print(circuit_problem.order_domain_values("c"))
    # test the backtracking method: 
    result = CSP.backtrack(circuit_csp)
    print(result)