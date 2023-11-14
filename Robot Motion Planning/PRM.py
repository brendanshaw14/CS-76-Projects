# class to handle the robot motion planner k-PRM
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot import Robot
# import the shapely class
from shapely.geometry import Point, Polygon, LineString

class PRM:
    def __init__(self, samples_per_dimension, num_neighbors, num_dimensions, obstacles):
        self.samples_per_dimension = samples_per_dimension # resolution of the PRM
        self.num_neighbors = num_neighbors # connectivity of the PRM (k)
        self.obstacles = obstacles # array of obstacles in the environment (shapely polygons)
        self.num_dimensions = num_dimensions # number of arm links
        self.samples = [] # list of samples
        self.adjacency_list = {} # graph represented as an adjacency list
        self.visited_from = {} # dictionary to keep track of which node a node was visited from
        self.step_size = 0.05 # step size for collision checking along the path

        self.uniform_dense_sample() # initialize the list of samples

    # collect the uniform dense samples
    def uniform_dense_sample(self):
        print("Generating samples...")
        # Get the number of samples to take per dimension
        current_sample = []
        self.uniform_dense_sample_recursive(current_sample)

    # recursive helper for uniform_dense_sample
    def uniform_dense_sample_recursive(self, current_sample):
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
            
    # build the graph using the adjacency list
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
        # Initialize an empty dict of distances
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
        num_steps = int(distance / self.step_size)
        # reset num steps if it is just 1
        if num_steps == 0:
            num_steps = 1
        # for each step
        for i in range(num_steps+1):
            # get the interpolated sample
            interpolated_sample = []
            for j in range(self.num_dimensions):
                interpolated_sample.append(sample1[j] + (sample2[j] - sample1[j]) * i / num_steps)
            # set the robot to the interpolated sample 
            robot = Robot(interpolated_sample, [1] * self.num_dimensions)
            # check if the interpolated sample is in collision
            if robot.check_collision(self.obstacles):
                # if it is, set the path to be invalid
                valid = False
                break
        # return whether or not the path is valid
        return valid

    # graph the adjacency list
    def graph(self, path=None):
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
            # if a path is provided
            if path: 
                # plot that path in a different color
                for i in range(len(path)-1):
                    ax.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], color='r')
            # show the plot
            plt.show()
        else: 
            print("cannot graph: incorrect dimensionality")

    # handle a query from the user for the planner
    def query(self, start, goal):
        # ensure valid start and goal states
        start_robot = Robot(start, [1] * self.num_dimensions)
        goal_robot = Robot(goal, [1] * self.num_dimensions)
        if start_robot.check_collision(self.obstacles) or goal_robot.check_collision(self.obstacles):
            print("start or goal is in collision")
            return None
        # if the start or goal node isn't in the graph, connect it to its nearest neighbor
        if start not in self.adjacency_list:
            self.connect_node_to_graph(start)
        if goal not in self.adjacency_list: 
            self.connect_node_to_graph(goal)
        # run the search algorithm
        return self.find_path(start, goal)
        
    # connect the start or goal node to the graph if it isn't already in it
    def connect_node_to_graph(self, node):
        # add the sample to self.samples
        self.samples.append(node)
        # start the new adjacency list
        self.adjacency_list[node] = []
        # for each other sample
        for other_sample in self.get_sample_distances(node):
            # if the sample is not the node of interest
            if node != other_sample:
                # if the there is a valid path
                if self.validate_path(node, other_sample):
                    self.adjacency_list[node].append(other_sample)
                    self.adjacency_list[other_sample].append(node)
                    break           

    # takes a start robot and an end robot, returning a path of robot configurations to connect them (adapted from Foxes and Chickens/uninformed_search.py)
    def find_path(self, start_state, goal_state):
        # initialize queue, add the start node
        queue = deque()
        queue.append(start_state)

        # visted satates set to avoid revisits
        visited_states = set() 
        visited_states.add(start_state)

        # track how many nodes have been visited and initialize the solution
        path = []

        # begin the search
        while queue: 
            # get the next node in queue and increment num_nodes_visited
            current = queue.popleft()

            # if this is the goal node, backchain 
            if current == goal_state: 
                path = self.backchain(current)
                return path

            # otherwise, get its unvisited successors and add them to the queue
            else: 
                for state in self.adjacency_list[current]:
                    # check if already visited
                    if state not in visited_states:
                        self.visited_from[state] = current
                        visited_states.add(state)
                        queue.append(state)
        return False


    # Backchain function for BFS to reconstruct the path
    def backchain(self, goal):
        path = []
        current = goal

        # Start from the goal node and follow parent references
        while current in self.visited_from:
            path.append(current)
            current = self.visited_from[current]
        path.append(current)

        # Reverse the path to get it in the correct order and return it
        path.reverse()
        return path
    
    def animate_robot_movement(self, path):
        fig, ax = plt.subplots()
        path_configs = []

        # get each robot's points and save them 
        xmax, ymax = 0, 0
        xmin, ymin = 0, 0
        for i in range(len(path)):
            robot = Robot(path[i], [1] * self.num_dimensions)
            points = robot.get_points()
            path_configs.append(points)
            for point in points:
                if point[0] > xmax:
                    xmax = point[0]
                if point[1] > ymax:
                    ymax = point[1]
                if point[0] < xmin:
                    xmin = point[0]
                if point[1] < ymin:
                    ymin = point[1]

        def update(frame):
            ax.clear()
            # Set initial axis limits based on obstacle positions
            ax.set_xlim(xmin + 1, xmax + 1)  # Adjust as needed
            ax.set_ylim(ymin + 1, ymax + 1)  # Adjust as needed


            # Draw obstacles (if applicable)
            for obstacle in self.obstacles:
                plt.plot(*obstacle.exterior.xy, color='black', linewidth=2, linestyle='-', alpha=0.5)

            # Draw robot arm
            robot = Robot(path[frame], [1] * self.num_dimensions)
            points = robot.get_points()

            for i in range(len(points) - 1):
                plt.plot([points[i][0], points[i + 1][0]], [points[i][1], points[i + 1][1]], marker='o', color='blue')

            plt.title('Robot Arm Movement')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.grid(True)
            # Return the iterable of Artists (in this case, an empty list)
            return []

        ani = FuncAnimation(fig, update, frames=len(path), interval=500, repeat=True)
        plt.show()



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
    # make some obstacles
    obstacles = []
    obstacles.append(Polygon([(0.5, 1.2), (0.5, 1.7), (0.3, 1.7), (0.3, 1.2)]))
    robot = Robot([0, 0], [1] * 2)
    obstacles.append(Polygon([(-0.2, -1), (-0.2, -0.5), (-0.5, -0.5), (-0.5, -1)]))
    robot.draw_robot_arm(obstacles=obstacles)

    motion_planner = PRM(samples_per_dimension=10, num_neighbors=10, num_dimensions=2, obstacles=obstacles)
    motion_planner.build_graph()
    path = motion_planner.query((0.5, 0.5), (3, 5))
    print(path)
    # motion_planner.graph(path=path)
    motion_planner.animate_robot_movement(path)

