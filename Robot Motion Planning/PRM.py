# class to handle the robot motion planner k-PRM
import numpy as np
import matplotlib.pyplot as plt
from robot import Robot
from mpl_toolkits.mplot3d import Axes3D

class PRM:
    def __init__(self, samples_per_dimension, num_neighbors, num_dimensions, obstacles):
        self.samples_per_dimension = samples_per_dimension # resolution of the PRM
        self.num_neighbors = num_neighbors
        self.obstacles = obstacles
        self.num_dimensions = num_dimensions
        self.samples = []
        self.edges = []
        self.adjacency_list = {}
        self.path = []
        self.uniform_dense_sample()

    def uniform_dense_sample(self, current_sample=None):
        # Get the number of samples to take per dimension
        current_sample = []
        self.uniform_dense_sample_recursive(current_sample)

    def uniform_dense_sample_recursive(self, current_sample, depth=0):
        # base case: if the index is num_dimensions, then we have assigned the last dimension
        if len(current_sample) == self.num_dimensions:
            # append the sample to the list of samples
            self.samples.append(tuple(current_sample))
            return
        # otherwise, we need to recurse and assign the next dimension
        # for each value in the number of samples per dimension
        for i in range(self.samples_per_dimension):
            # make a copy of the current sample
            current_sample_copy = current_sample.copy()
            # add the next value
            current_sample_copy.append((i / self.samples_per_dimension) * 2 * np.pi)
            # pass it to the next recursive call
            self.uniform_dense_sample_recursive(current_sample_copy)
            
    def build_graph(self):
        # for each sample in the list of samples
        for sample in self.samples:
            robot = Robot(sample, [1] * self.num_dimensions)
            # check if the sample is in collision
            if not robot.check_collision(self.obstacles):
                # add the sample to the adjacency list
                self.adjacency_list[sample] = []
                # for each other sample in the list of samples
                for other_sample in self.samples:
                    # if the sample is not the other sample
                    if sample != other_sample:
                        # check if the edge is valid
                        if self.validate_path(sample, other_sample):
                            # if it is, add it to the adjacency list
                            self.adjacency_list[sample].append(other_sample)

    # check that the path between two samples is valid
    def validate_path(self, sample1, sample2): 
        # initialize the path to be valid
        valid = True
        # initialize the robot
        robot = Robot(sample1, [1] * self.num_dimensions)
        # get the distance between the samples
        distance = get_distance(sample1, sample2)
        # get the number of steps to take
        num_steps = int(distance / 0.1)
        # for each step
        for i in range(num_steps):
            # get the interpolated sample
            interpolated_sample = []
            for j in range(self.num_dimensions):
                interpolated_sample.append(sample1[j] + (sample2[j] - sample1[j]) * i / num_steps)
            # check if the interpolated sample is in collision
            if robot.check_collision(self.obstacles):
                # if it is, set the path to be invalid
                valid = False
                break
        # return whether or not the path is valid
        return valid

    def get_sample_distances(self, sample):
        # initialize empty list of distances
        distances = {}
        # for each other sample in the list of samples
        for other_sample in self.samples:
            # if the sample is not the other sample
            if sample != other_sample:
                # if it is, add it to the distances list
                distances[other_sample] = get_distance(sample, other_sample)
        # sort the dictionary of distances by the distance
        distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        # return the list of distances
        return distances
    
def get_distance(sample1, sample2): 
    # initialize the distance to 0
    distance = 0
    # for each dimension
    for i in range(len(sample1)):
        # add the squared difference in the dimension
        distance += (sample1[i] - sample2[i]) ** 2
    # return the square root of the distance
    return np.sqrt(distance)

# main
if __name__ == "__main__":
    motion_planner = PRM(samples_per_dimension=10, num_neighbors=10, num_dimensions=3, obstacles=[])
    print((motion_planner.samples))