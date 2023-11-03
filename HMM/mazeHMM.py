# HMM for the color sensor robot mazeworld
# By Brendan Shaw, 2023
# Written for the HMM project for CS76
import Maze

class MazeHMM:

    def __init__ (self, maze):
        self.maze = maze
        self.transitions = {}
        self.emissions = {}
        self.distribution = {}

    # initialize the probability distribution to be evenly since we don't know the robot's start location 
    def initialize_start_distribution(self):
        # for each location in the maze, add it to the distribution with a probability of 1/total number of locations
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                self.distribution[(x, y)] = 1 / (self.maze.width * self.maze.height)

# main
if __name__ == "__main__":
    maze = Maze.Maze("HMM/maze1.maz") 
    hmm = MazeHMM(maze)
    hmm.initialize_start_distribution()
    print(hmm.maze, hmm.distribution)
