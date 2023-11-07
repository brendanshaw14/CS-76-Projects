# HMM for the color sensor robot mazeworld
# By Brendan Shaw, 2023
# Written for the HMM project for CS76
#   Uses the Maze class from COSC 76 Materials
import Maze
import random
import numpy as np
import pygame
import sys

class GUIHMM:

    # Constants
    WIDTH, HEIGHT = 800, 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    colors = {'g' : (0, 255, 0), 'y' : (255, 255, 0), 'r' : (255, 0, 0), 'b' : (0, 0, 255)}

    def __init__ (self, maze):
        self.maze = maze
        # set the square size to be the minimum of the maze's width and height
        self.square_size = min(self.WIDTH/2 // self.maze.width, self.HEIGHT/2 // self.maze.height)
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
        move = None
        while not valid_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False
                    elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        move = event.key
                        valid_key = True
                        break
                    else:
                        print("Invalid key")

        # get the new location
        if move is not None:
            new_location = [self.maze.robotloc[0] + moves[chr(move)][0], self.maze.robotloc[1] + moves[chr(move)][1]]
            # make sure the move is valid
            if self.maze.is_floor(new_location[0], new_location[1]):
                # update the robot's location
                self.maze.robotloc = new_location
            print("Moving robot to location " + str(self.maze.robotloc) + " with color " + str(self.maze.get_color(self.maze.robotloc[0], self.maze.robotloc[1])))

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
        self.initialize_pygame()
        # print start state
        print("Initial Maze:\n" + str(self.maze))
        print("Initial Distribution:\n " + self.dist_to_string()) 
        print(self.transition_probabilities)
        
        # initialize the loop
        running = True
        while running:
            # use the current state to predict the next state with transition probabilities
            self.predict()
            # get the user's next move and update the robot's location with it 
            if not self.get_next_location():
                print("Quitting...")
                running = False

            # get the sensor's reading based on the new location
            emission = self.get_sensor_emission()
            # udpate the distribution 
            self.update(emission)
            print("Color Emitted: " + emission + "\n" + maze.get_colored_maze())
            print("Maze:\n" + str(self.maze))
            print("Distribution:\n " + self.dist_to_string())
            self.redraw_screen(self.window)

        # quit the gui
        pygame.quit()
        sys.exit()
    
    def dist_to_string(self):
        reshaped_dist = np.reshape(self.distribution, (self.maze.height, self.maze.width), order='C')[::-1]
        return str(reshaped_dist)

    def initialize_pygame(self):
        # Initialize Pygame
        pygame.init()

        # Initialize Pygame window
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Solver")
        self.window.fill(self.WHITE)

        # Draw maze
        self.redraw_screen(self.window)
        pygame.display.flip()
        

    def redraw_screen(self, window):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Draw the maze (colored squares)
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    color = self.colors[self.maze.get_color(x, y)]
                else:
                    color = self.BLACK
                # Calculate the correct y-coordinate based on maze height
                x_coord = x * self.square_size + (400-self.maze.width*self.square_size)
                y_coord = (self.maze.height - 1 - y) * self.square_size + 200
                # Fill the rectangle with the specified color
                pygame.draw.rect(window, color, (x_coord, y_coord, self.square_size, self.square_size))
                # Set width parameter to 1 for a black stroke
                pygame.draw.rect(window, self.BLACK, (x_coord, y_coord, self.square_size, self.square_size), 1)

        # Draw the robot (a dot) at its current location
        robot_x, robot_y = maze.robotloc
        pygame.draw.circle(window, (255, 255, 255), (robot_x * self.square_size + 400-self.maze.width*self.square_size + self.square_size//2, (self.maze.height - 1 - robot_y) * self.square_size + self.square_size//2 + 200), 5)

        # Draw the probability distribution (opacity indicates probability)
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                index = y * self.maze.width + x
                probability = self.distribution[index]
        
                # Calculate color with opacity based on probability
                # scale the probability so that the minimum value is black and the maximum value is colored
                scaled_probability = (probability - self.distribution.min()) / (self.distribution.max() - self.distribution.min())
                opacity = int(scaled_probability * 255)  # Calculate opacity based on probability
        
                # Calculate rectangle position and size for the right half of the screen
                rect_x = x * self.square_size + 400
                rect_y = (self.maze.height - 1 - y) * self.square_size + 200
                rect_width = self.square_size
                rect_height = self.square_size
        
                # Draw rectangle with black stroke and purple fill with transparency
                pygame.draw.rect(window, (255-opacity, 255- opacity, 255 - opacity), (rect_x, rect_y, rect_width, rect_height))  # Purple fill with transparency
                pygame.draw.rect(window, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), 1)  # Black stroke

                # Update the display
                pygame.display.flip()


# main
if __name__ == "__main__":
    maze = Maze.Maze("HMM/maze6.maz") 
    hmm = GUIHMM(maze)
    # print the transition probabilities instance variable in a readable format with even spacing
    hmm.run()
