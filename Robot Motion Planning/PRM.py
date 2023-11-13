# class to handle the robot motion planner k-PRM
import numpy as np
import matplotlib.pyplot as plt
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
            

# main
if __name__ == "__main__":
    motion_planner = PRM(samples_per_dimension=10, num_neighbors=10, num_dimensions=3, obstacles=[])
    print((motion_planner.samples))