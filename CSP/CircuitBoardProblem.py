# Circuit BOard Problem for CSP input

from CSP import CSP

class CircuitBoardProblem:

    # constructor
    def __init__(self, components, board_length, board_width):
        self.components = components
        self.board_length = board_length
        self.board_width = board_width

    # TODO: 
    # *******is_assignment_complete********""
    #   -returns whether or not the assignment is the same lenght
    #    as thenumber of variables, ensuring that every variable has an assignment
    # returns true if all the variables have been assigned
    def is_assignment_complete(self, assignment): 
        # if the length of the assignment is the same as the number of countries
        if len(assignment) == len(self.countries): 
            return True
        return False
    
    # TODO: 
    # chooses the next variable to be used by the CSP solver
    def choose_next_variable(self, assignment): 
        #loop through countries
        for country in self.countries: 
            # if the country hasn't been assigned
            if country not in assignment:
                # return it to be visited next
                return country
    
    # TODO: add ordering (return the valid ones first)
    # *******order_domain_values********""
    #   -returns the next value in the domain to search
    def order_domain_values(self, variable):
        # just return the list of available colors in this case
        return self.colors
        
    # TODO: 
    # *******is_consistent********""
    #   -returns whether or not giving the input variable the input 
    #   value is within the constraints of the problem. 
    def is_consistent(self, assignment, variable, value):




if __name__ == "__main__":
    pass
