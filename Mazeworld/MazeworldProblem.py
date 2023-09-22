from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    # TODO: write the get_successors function here
    def get_successors(self, state):
        # make sure there are whole robots (an even number of values in the tuple)
        if len(state) % 2 != 0: 
            return None

        # initialize empty successor set and movements set
        successors = []
        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # for each robot-  we want to move just that robot, not the others
        for i in range(0, len(state), 2):
            # get current robot's x and y
            x, y = state[i], state[i+1]
            # for each action
            for dx, dy in actions:
                new_x, new_y = x + dx, y + dy
    
                if self.maze.is_floor(new_x, new_y): 
                    # Copy the current state into a list
                    successor = list(state)
                    # Change the current robots location
                    successor[i], successor[i+1] = new_x, new_y
                    #convert back to a tuple
                    successors.append(tuple(successor))

        return successors

    # TODO: write the goaltest function here
    def goal_test(self, state):
        return False

    # TODO: write the heuristic function somewhere (not here)
    def manhattan_heuristic(node):
        #
        return 10

## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2)))
