from Maze import Maze
from time import sleep
from astar_search import *

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        # store the maze, the start state (first index is which robot's turn it is, then coords of robots), then goal locations
        self.maze = maze
        self.goal_locations = goal_locations
        self.num_robots = int(len(self.maze.robotloc)/2)
        self.start_state = (0,)
        self.start_state += tuple(self.maze.robotloc)

    def __str__(self):
        string =  "Mazeworld problem: \n"
        string += "Number of Robots: " + str(self.num_robots) + "\n"
        string += "Start State: " + str(self.start_state) + "\n"
        string += "Goal Locations: " + str(self.goal_locations) + "\n"
        string += " ------------------------"
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


    def get_successors(self, state):
        # initialize empty successor set and movements set, including passing on the turn
        successors = []

        # determine whether or not to include just switching the turn as an action
        if len(state) > 3: actions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
        else: actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # get which robot's turn it is - this is the first value
        robot_turn = state[0]
        robot_index = robot_turn * 2 + 1 

        # get current robot's x and y
        x, y = state[robot_index], state[robot_index+1]

        # for each action
        for dx, dy in actions:
            #apply the action
            new_x, new_y = x + dx, y + dy
            # print(x, y, new_x, new_y)
            # if the new location is a floor and doesn't have a robot in it 
            if self.maze.is_floor(new_x, new_y) and not (self.maze.has_robot(new_x, new_y)): 
                # print(x, y, new_x, new_y)
                # Copy the current state into a list
                successor = list(state) 

                # update which robot's turn it is
                if successor[0] == self.num_robots - 1: successor[0] = 0
                else: successor[0] += 1

                # update the robot's location
                successor[robot_index], successor[robot_index+1] = new_x, new_y # Change the current robots location
                successors.append(tuple(successor)) #convert back to a tuple

        return successors

    # returns true if every robot is in a goal location
    def goal_test(self, state):
        print(state)
        goal_locations = list(self.goal_locations)
        # loop through the number of robots
        for i in range(self.num_robots):
            # get the current robot
            robot_index = i * 2 + 1 
            robot_location = (state[robot_index], state[robot_index+1])
            # if that robot is not in a goal location
            if robot_location not in goal_locations: 
                return False
            # remove that goal location from the liast
            goal_locations.remove(robot_location)
        return True

    # TODO: write the heuristic function somewhere (not here)
    def manhattan_heuristic(node):
        #
        return 10

## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze2 = Maze("Mazeworld/maze2.maz")
    test_maze3 = Maze("Mazeworld/maze3.maz")
    test_mp2 = MazeworldProblem(test_maze2, [(2, 2)])
    test_mp3 = MazeworldProblem(test_maze3, [(2, 2), (3, 0)])
    print(str(test_mp2))
    print(str(test_mp3))

    # one robot tests: these are all passed
    print(test_mp2.get_successors((0, 1, 0))) # should be [(0, 1, 1)]
    print(test_mp2.get_successors((0, 2, 1))) # should be [(0, 1, 1), (0, 3, 1), (0, 2, 2)]
    print(test_mp2.get_successors((0, 3, 1))) # should be [(0, 3, 0), (0, 2, 1)]
    print(test_mp2.get_successors((0, 3, 0))) # should be [(0, 3, 1))]
    print(test_mp2.get_successors((0, 2, 2))) # should be [(0, 2, 1)]

    # two robot tests: all passed
    print("------------------")
    print(test_mp3.get_successors((0, 1, 0, 1, 1))) # should be [(1, 1, 1, 1, 1)]
    print(test_mp3.get_successors((1, 1, 0, 1, 1))) # should be [(0, 1, 0, 1, 1), (0, 1, 0, 2, 1)]

    # test robot collisions
    print(test_mp2.get_successors((0, 1, 1))) # should be [(0, 2, 1)]

    print("------------------")
    # test the goal_test function
    print(test_mp2.goal_test((0, 2, 2))) # should be true
    print(test_mp2.goal_test((0, 2, 1))) # should be false
    print(test_mp3.goal_test((0, 2, 2, 1, 1))) # should be false
    print(test_mp3.goal_test((0, 2, 2, 3, 0))) # should be true
    print(test_mp3.goal_test((0, 2, 1, 3, 0))) # should be false
    print(test_mp3.goal_test((0, 2, 2, 2, 2))) # should be false