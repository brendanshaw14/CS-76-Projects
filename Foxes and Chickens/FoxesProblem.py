class FoxesProblem:
    # global variables
    actions = [(-2, 0, -1), (-1, 0, -1), (-1, -1, -1), (0, -1, -1), (0, -2, -1)]

    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        successors = list()
        if state[2] == 1:
            for action in self.actions:
                successor = ((state[0]+action[0], state[1]+action[1], 0))
                if self.is_valid_state(successor) and successor != self.start_state:
                    successors.append(successor)
        else:
            for action in self.actions:
                successor = (state[0]-action[0], state[1]-action[1], 1)
                if self.is_valid_state(successor) and successor != self.start_state:
                    successors.append(successor)
        return successors

    def is_valid_state(self, state):
        # is the left side good? 
        if self.start_state[0] >= state[0] >= 0 and self.start_state[1] >= state[1] >= 0 and state[2] >= 0:
            if (state[0] <= state[1]) or state[1] == 0: 
                #is the right side good?
                if (self.start_state[0] - state[0]) <= (self.start_state[1]-state[1]) or (self.start_state[1] - state[1]) == 0:
                    return True
        return False


    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

# tests
if __name__ == "__main__":
    test1= FoxesProblem((3, 3, 1))
    print(test1.get_successors((3, 3, 1)))
    print(test1.get_successors((2, 2, 0)))
    print(test1.get_successors((2, 3, 1)))
    print(test1.get_successors((0, 3, 0)))
    print(test1.get_successors((1, 3, 1)))
    print(test1.get_successors((1, 1, 0)))
    print(test1.get_successors((2, 2, 1)))
    print(test1.get_successors((2, 0, 0)))
    print(test1.get_successors((3, 0, 1)))
    print(test1.get_successors((1, 0, 0)))
    print(test1.get_successors((1, 1, 1)))

