# class to handle the robot motion planner k-PRM
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from robot import Robot
# import the shapely class
from shapely.geometry import Point, Polygon, LineString

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
                k = 0
                # for each other sample in the list of samples
                for other_sample in self.get_sample_distances(sample):
                    # if the sample is not the other sample
                    if sample != other_sample:
                        # check if the edge is valid
                        if self.validate_path(sample, other_sample):
                            # if it is, add it to the adjacency list
                            self.adjacency_list[sample].append(other_sample)
                            k += 1
                            if k == self.num_neighbors:
                                break
            
    # sort samples by distance
    def get_sample_distances(self, sample):
        # Initialize an empty list of distances
        distances = {}
        # For each other sample in the list of samples
        for other_sample in self.samples:
            # If the sample is not the other sample
            if sample != other_sample:
                # Calculate and store the distance in the distances dictionary
                distances[other_sample] = get_distance(sample, other_sample)
        # Sort the dictionary items by the distance value and get the keys
        sorted_keys = [k for k, _ in sorted(distances.items(), key=lambda item: item[1])]
        # Return the list of keys sorted by distance
        return sorted_keys
    
    # check that the path between two samples is valid
    def validate_path(self, sample1, sample2): 
        # initialize the path to be valid
        valid = True
        # initialize the robot
        robot = Robot(sample1, [1] * self.num_dimensions)
        # get the distance between the samples
        distance = get_distance(sample1, sample2)
        # get the number of steps to take
        num_steps = int(distance / 0.05)
        print(num_steps)
        # for each step
        for i in range(num_steps+1):
            # get the interpolated sample
            interpolated_sample = []
            for j in range(self.num_dimensions):
                interpolated_sample.append(sample1[j] + (sample2[j] - sample1[j]) * i / num_steps)
            # set the robot to the interpolated sample 
            robot = Robot(interpolated_sample, [1] * self.num_dimensions)
            # check if the interpolated sample is in collision
            print(robot.angles)
            if robot.check_collision(self.obstacles):
                # if it is, set the path to be invalid
                valid = False
                break
        # return whether or not the path is valid
        return valid

    # graph the adjacency list
    def graph(self):
        # graph the adjacency list, assuming 2D samples
        if self.num_dimensions == 2:
            # initialize the figure
            fig, ax = plt.subplots()
            # for each sample in the list of samples
            for sample in self.samples:
                # for each other sample in the list of samples
                if sample in self.adjacency_list:
                    ax.plot(sample[0], sample[1], 'o', color='k')
                    for other_sample in self.adjacency_list[sample]:
                        # plot a line between the samples
                        ax.plot([sample[0], other_sample[0]], [sample[1], other_sample[1]], color='k')
            # show the plot
            plt.show()

    def query(self, start, goal):
        # if the start or goal node isn't in the graph, connect it to its nearest neighbor
        if start not in self.adjacency_list:
            self.connect_node_to_graph(start)
        if goal not in self.adjacency_list: 
            self.connect_node_to_graph(goal)

    def connect_node_to_graph(self, node):
        # start the new adjacency list
        self.adjacency_list[node] = []
        # for each other sample
        for other_sample in self.get_sample_distances(node):
            # if the sample is not the node of interest
            if node != other_sample:
                # if the there is a valid path
                if self.validate_path(node, other_sample):
                    self.adjacency_list[node].append(other_sample)
                    break           

# takes a start robot and an end robot, returning a path of robot configurations to connect them (adapted from Foxes and Chickens/uninformed_search.py)
    def search(self, start_state, goal_state):
        # initialize queue, add the start node
        queue = deque()
        queue.append(start_state)

        # visted satates set to avoid revisits
        visited_states = set() 
        visited_states.add(start_state)

        # track how many nodes have been visited and initialize the solution
        path = []
        num_nodes_visited = 0

        # begin the search
        while queue: 
            # get the next node in queue and increment num_nodes_visited
            current = queue.popleft()
            num_nodes_visited += 1

            # if this is the goal node, backchain 
            if current.state == goal_state: 
                path = backchain(current)
                return path

            # otherwise, get its unvisited successors and add them to the queue
            else: 
                for state in self.adjacency_list[current.state]:
                    # check if already visited
                    if state not in visited_states:
                        visited_states.add(current.state)
                        queue.append(state)
        return False


# Backchain function for BFS to reconstruct the path
def backchain(goal):
    path = []
    current_node = goal

    # Start from the goal node and follow parent references
    while current_node is not None:
        path.append(current_node.state)
        current_node = current_node.parent

    # Reverse the path to get it in the correct order and return it
    path.reverse()
    return path


# retrieve the distance between two samples
def get_distance(sample1, sample2): 
    # initialize the distance to 0
    distance = 0
    # for each dimension
    for i in range(len(sample1)):
        # if the difference is less than pi
        if abs(sample1[i] - sample2[i]) < np.pi:
            # add the squared difference in the dimension
            distance += (sample1[i] - sample2[i]) ** 2
        # if the difference is greater than pi
        else:
            # add the squared difference in the dimension
            distance += (2 * np.pi - abs(sample1[i] - sample2[i])) ** 2
    # return the square root of the distance
    return np.sqrt(distance)


# main
if __name__ == "__main__":
    obstacle_polygon = Polygon([(0.5, 0.5), (0.5, 0.7), (0.3, 0.7), (0.3, 0.5)])
    obstacles = [obstacle_polygon]

    motion_planner = PRM(samples_per_dimension=30, num_neighbors=10, num_dimensions=2, obstacles=obstacles)
    motion_planner.build_graph()
    motion_planner.graph()


