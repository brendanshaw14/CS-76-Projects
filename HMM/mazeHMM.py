# HMM for the color sensor robot mazeworld
# By Brendan Shaw, 2023
# Written for the HMM project for CS76
#   Uses the Maze class from COSC 76 Materials
import Maze
import random
import numpy as np

class MazeHMM:

    def __init__ (self, maze):
        self.maze = maze
        self.emissions = {}
        # initialize self.distribution to be an empty numpy matrix
        self.distribution = np.zeros((self.maze.width, self.maze.height))
        # initialize the probability distribution evenly since we don't know anything yet
        self.initialize_start_distribution()
        # initialize self.transition probabilities to be an empty numpy matrix that is the size of the entire maze squared
        self.transition_probabilities = np.zeros((self.maze.width * self.maze.height, self.maze.width * self.maze.height))
        self.initialize_transition_probabilities()
    
    # initialize the transition probabilities
    def initialize_transition_probabilities(self):
        # for each index in the transition probabilities matrix
        for i in range(self.maze.width * self.maze.height):
            # get the x and y coordinates of the index
            x = i % self.maze.width
            y = i // self.maze.width
            # for each adjacent spot to this index:
            

            for j in range(self.maze.width * self.maze.height):
                # get the x and y coordinates of the other spot
                x2 = j % self.maze.width
                y2 = j // self.maze.width
                # if the other spot is adjacent to the current spot
                if abs(x - x2) + abs(y - y2) == 1:
                    # if the other spot is a floor tile:
                    if self.maze.is_floor(x2, y2):
                        # increment the current spot's probability of transition to itself (not moving) by 0.25
                        self.transition_probabilities[i][i] += 0.25
                    # if not a floor tile:
                    else:
                        # set the transition probability to 0.25
                        self.transition_probabilities[i][j] = 0.25
                # if not adjacent:
                else:
                    # set the transition probability to 0
                    self.transition_probabilities[i][j] = 0

    # initialize the probability distribution to be evenly since we don't know the robot's start location 
    def initialize_start_distribution(self):
        # for each location in the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # set the numpy matrix at that location to be 1 / (width * height)
                self.distribution[x][y] = 1 / (self.maze.width * self.maze.height)

    # get the user's next move
    def get_next_location(self):
        moves = {"w": (0, 1), "a": (-1, 0), "s": (0, -1), "d": (1, 0)}
        # prompt the user to type w, a, s, or d to move the robot
        move = input("Enter w, a, s, or d to move the robot: ")
        # move the robotloc in the maze using move
        new_location = [self.maze.robotloc[0] + moves[move][0], self.maze.robotloc[1] + moves[move][1]]
        # make sure the move is valid
        if self.maze.is_floor(new_location[0], new_location[1]):
            # update the robot's location
            self.maze.robotloc = new_location
        # update the probability distribution based on the sensor reading

    # get the sensor's reading based on the robot's location 
    def get_sensor_emission(self):
        # get the color of the robot's current location
        color = self.maze.get_color(self.maze.robotloc[0], self.maze.robotloc[1])
        # get the probability of the sensor reading the color of the robot's current location
        # return the same color as the color with 88% probability
        if random.random() < 0.88:
            return color
        # return a random one of the other three colors with 0.04 probability each
        else:
            return random.choice("rygb".replace(color, ""))
    
    def filtering_algorithm(self): 
        # get the user's next move and update the robot's location with it 
        self.get_next_location()
        # get the sensor's reading based on the new location
        emission = self.get_sensor_emission()


# main
if __name__ == "__main__":
    maze = Maze.Maze("HMM/maze1.maz") 
    hmm = MazeHMM(maze)
    print(hmm.maze, hmm.distribution)
    print(hmm.maze.colors_map)
    # print the transition probabilities instance variable in a readable format with even spacing
    for row in hmm.transition_probabilities:
        print(row)
    # print the start distribution instance variable in a readable format with even spacing