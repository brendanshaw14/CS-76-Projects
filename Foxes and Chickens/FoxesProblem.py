class FoxesProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        successors = list()
        actions = [(-2, 0, -1), (-1, 0, -1), (-1, -1, -1), (0, -1, -1), (0, -2, -1)]
        if state[2] == 1:
            for action in actions:
                foxes = state[0]+action[0]
                chickens = state[1]+action[1]
                if foxes >= 0 and chickens >= 0: 
                    successors.append((foxes, chickens, 0))
        else:
            for action in actions:
                foxes = state[0]+action[0]
                chickens = state[1]+action[1]
                if foxes >= 0 and chickens >= 0: 
                    successors.append((foxes, chickens, 1))
        return successors

    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

# tests
if __name__ == "__main__":
    test1= FoxesProblem((3, 3, 1))
    print(test1.get_successors((3, 3, 1)))

    test2= FoxesProblem((2, 1, 0))
    print(test2.get_successors((2, 1, 0)))
