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
        # initialize self.distribution to be an empty numpy matrix
        self.distribution = np.zeros((self.maze.width*self.maze.height))
        # initialize the probability distribution evenly since we don't know anything yet
        self.initialize_start_distribution()
        # initialize self.transition probabilities to be an empty numpy matrix that is the size of the entire maze squared
        self.transition_probabilities = np.zeros((self.maze.width * self.maze.height, self.maze.width * self.maze.height))
        self.initialize_transition_probabilities()
        # initialize print settings
        np.set_printoptions(precision=4, suppress=True, linewidth=100)
    
    # initialize the transition probabilities
    def initialize_transition_probabilities(self):
        actions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        # for each index in the transition probabilities matrix
        for i in range(self.maze.width * self.maze.height):
            # get the x and y coordinates of the index
            x = i % self.maze.width
            y = i // self.maze.width
            # skip if not a floor
            if not self.maze.is_floor(x, y):
                continue
            # for each adjacent spot to this index:
            for action in actions:
                # get the x and y coordinates of the adjacent spot
                new_x, new_y = x + action[0], y + action[1]
                # if that spot is a floor:
                if self.maze.is_floor(new_x, new_y):
                    # calculate the index of this spot in the array
                    index = new_y * self.maze.width + new_x 
                    # set the probability of moving there to 0.25
                    self.transition_probabilities[i, index] = 0.25
                # if that spot is not a floor:
                else:
                    # increment the probability of not moving at all by 0.25 
                    self.transition_probabilities[i, i] += 0.25



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
                    self.distribution[maze.width * y + x] = 1 / floorspace

    # multiply the probability distribution by the transition probabilities
    def predict(self): 
        # multiply each column in the transition probabilities matrix by the probability distribution value for that that index
        new_distribution = np.matmul(self.transition_probabilities, self.distribution)
        # Normalize the new distribution
        self.distribution = new_distribution / new_distribution.sum()


    # get the user's next move
    def get_next_location(self):
        moves = {"w": (0, 1), "a": (-1, 0), "s": (0, -1), "d": (1, 0), "q": (0, 0)}
        valid_key = False
        # prompt the user to type w, a, s, or d to move the robot
        move = input("Enter w, a, s, or d to move the robot; q to quit: ")
        while not valid_key:
            if move in moves:
                valid_key = True
                break
            else:
                print("Invalid key")
            move = input("Enter w, a, s, or d to move the robot; q to quit: ")
        # if the use quits, return False
        if move == "q":
            return False
        # otherwise, update the robot's location
        else:
            # get the new location
            new_location = [self.maze.robotloc[0] + moves[move][0], self.maze.robotloc[1] + moves[move][1]]
            print("Moving robot to location " + str(new_location) + " with color " + str(self.maze.get_color(new_location[0], new_location[1])))
            # make sure the move is valid
            if self.maze.is_floor(new_location[0], new_location[1]):
                # update the robot's location
                self.maze.robotloc = new_location
            return True

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

    # function to update the tribution based on the sensor's reading
    def update(self, emission):
        # for each state
        for i in range(self.maze.width * self.maze.height):
            # get the x and y coordinates of the state
            x = i % self.maze.width
            y = i // self.maze.width
            # if the state is a floor
            if self.maze.is_floor(x, y):
                # get the color of the state
                color = self.maze.get_color(x, y)
                # if the color of the state matches the sensor's reading
                if color == emission:
                    # multiply the probability distribution by 0.88
                    self.distribution[i] *= 0.88
                # if the color of the state does not match the sensor's reading
                else:
                    # multiply the probability distribution by 0.04
                    self.distribution[i] *= 0.04
        # calculate the total sum of probabilities using NumPy sum function
        total = np.sum(self.distribution)
        # divide the entire array by the total using broadcasting
        self.distribution /= total

    # main event loop
    def run(self): 

        # print start state
        print("Initial Maze:\n" + str(self.maze))
        print("Initial Distribution:\n " + self.dist_to_string()) 
        print(self.transition_probabilities)
        
        # initialize the loop
        while True:
            # use the current state to predict the next state with transition probabilities
            self.predict()
            # get the user's next move and update the robot's location with it 
            if not self.get_next_location():
                print("Quitting...")
                return False
            # get the sensor's reading based on the new location
            emission = self.get_sensor_emission()
            # udpate the distribution 
            self.update(emission)
            print("Color Emitted: " + emission + "\n" + maze.get_colored_maze())
            print("Maze:\n" + str(self.maze))
            print("Distribution:\n " + self.dist_to_string())
    
    def dist_to_string(self):
        reshaped_dist = np.reshape(self.distribution, (self.maze.height, self.maze.width), order='C')[::-1]
        return str(reshaped_dist)



# main
if __name__ == "__main__":
    maze = Maze.Maze("HMM/maze6.maz") 
    hmm = MazeHMM(maze)
    # print the transition probabilities instance variable in a readable format with even spacing
    hmm.run()
