class FoxesProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        """
        if the boat is on the left:
            Action States: 
                (-2, 0, -1)
                (-1, 0, -1)
                (-1, -1, -1)
                (0, -1, -1)
                (0, -2, -1)
        if the boat is not on the left:
            Action States: 
                -(-2, 0, -1)
                -(-1, 0, -1)
                -(-1, -1, -1)
                -(0, -1, -1)
                -(0, -2, -1)
        """
        successors = list()
        actions = [(-2, 0, -1), (-1, 0, -1), (-1, -1, -1), (0, -1, -1), (0, -2, -1)]
        if state[2] == 1:
            for action in actions:
                successors.append((state[0]+action[0], state[1]+action[1], state[2]+action[2]))
        else:
            for action in actions:
                successors.append((state[0]-action[0], state[1]-action[1], state[2]-action[2]))
        return successors
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list

    # I also had a goal test method. You should write one.
    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

# tests
if __name__ == "__main__":
    test1= FoxesProblem((3, 3, 1))
    test2 = FoxesProblem((3, 3, 0))
    print(test1.get_successors((3, 3, 1)))
    print(test2.get_successors((3, 3, 0)))
