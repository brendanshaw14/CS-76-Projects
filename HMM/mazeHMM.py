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
        actions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        # for each index in the transition probabilities matrix
        for i in range(self.maze.width * self.maze.height):
            # get the x and y coordinates of the index
            x = i % self.maze.width
            y = i // self.maze.width
            print(x, y)
            # for each adjacent spot to this index:
            for action in actions:
                # get the x and y coordinates of the adjacent spot
                new_x, new_y = x + action[0], y + action[1]
                # if that spot is a floor:
                if self.maze.is_floor(new_x, new_y):
                    # calculate the index of this spot in the array
                    index = new_y * self.maze.width + new_x 
                    # set the probability of moving there by 0.25
                    self.transition_probabilities[i][index] = 0.25
                # if that spot is not a floor:
                else:
                    # increment the probability of not moving at all by 0.25 
                    self.transition_probabilities[i][i] += 0.25



    # initialize the probability distribution to be evenly since we don't know the robot's start location 
    def initialize_start_distribution(self):
        # keep track of maze floorspace
        floorspace = 0
        # for each location in the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the location is a floor
                if self.maze.is_floor(x, y):
                    # increment floorspace
                    floorspace += 1
        # for each location in the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the location is a floor, set the numpy matrix at that location to be 1 / (width * height)
                if self.maze.is_floor(x, y):
                    self.distribution[self.maze.height - y - 1][x] = 1 / (floorspace)

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

    # multiply the probability distribution by the transition probabilities
    def predict(self): 
        # reshape the probability distribution to be a column vector
        self.distribution.reshape(16, 1)
        print(self.distribution)



# main
if __name__ == "__main__":
    maze = Maze.Maze("HMM/maze1.maz") 
    hmm = MazeHMM(maze)
    print(hmm.maze, hmm.distribution)
    print(hmm.maze.colors_map)
    # print the transition probabilities instance variable in a readable format with even spacing
    np.set_printoptions(precision=4, suppress=True, linewidth=100)
    print(hmm.transition_probabilities)
    hmm.predict()