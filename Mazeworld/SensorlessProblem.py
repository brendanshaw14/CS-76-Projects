from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze, goal_locations):
        self.maze = maze 
        self.goal_locations = goal_locations 
        self.start_state = self.get_start_state()

    def __str__(self):
        string =  "Blind robot problem: \n"
        string += "Goal location: "
        strin += str(self.goal_location) + "\n"
        return string

    def goal_test(self, state): 
        # if there's only one state in the set 
        if len(state) == 1: 
            # if that state is the goal location return true
            if state[0] in self.goal_locations: return True 
        return False
            

    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))

    def get_start_state(self): 
        #initialize the set
        possible_locations = []

        # iterate through all coordinates in the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the coordinate is a floor coordinate, add it as a possible coordinate to the state
                if self.maze.is_floor(x, y): 
                    possible_locations.append((x, y))
        return possible_locations 

                    


    # return the valid successor states for a given state
    def get_successors(self, state): 
        # STATE IS A LIST OF TUPLES
        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        successors = []
        # for each action 
        for dx, dy in actions:
            # make a new set of belief states
            belief_state = set()
            # for every location in the current state
            for x, y in state: 
                # get the potential successor node's coordinates
                new_x, new_y = x + dx, y + dy
                # if the node can move
                if self.maze.is_floor(new_x, new_y):
                    # add that tile to the successor belief state
                    belief_state.add((new_x, new_y))
                # if it can't move
                else: 
                    # add it's current tile to the successor belief state
                    belief_state.add((x, y))
            # add this belief state to the set of total states
            successors.append((list(belief_state)))
        # return a set of sets of tuples 
        return successors
            

## A bit of test code

if __name__ == "__main__":
    test_maze1 = Maze("Mazeworld/mazes/maze1.maz")
    test_problem1 = SensorlessProblem(test_maze1, [(2, 2)])

    # # test the get_start_state method
    print(test_problem1.start_state)

    # test the goal_teset method
    print(test_problem1.goal_test([(2, 2)])) # should be true
    print(test_problem1.goal_test([(2, 2, 3, 3, 4, 4, 5, 5)])) # should be false
    print(test_problem1.goal_test([(2, 3)])) # should be false
    
    # test get_successors: passed
    successors = test_problem1.get_successors(test_problem1.start_state)
    expected = [[(1, 1), (2, 2), (3, 1)], [(1, 0), (2, 1), (3, 0)], [(1, 0), (2, 1), (2, 2), (3, 0), (3, 1)], [(1, 0), (1, 1), (2, 1), (2, 2), (3, 0)]]
