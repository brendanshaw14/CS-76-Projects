import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from shapely import affinity

class Robot:
    def __init__(self, num_links, link_lengths):
        self.num_links = num_links
        self.link_lengths = link_lengths

    # initialize self.points to be a list of points that represent the robot arm using the angles and lengths
    def get_points(self):
        # initialize empty list, x and y to be 0
        points = []
        x, y = 0, 0 
        points.append((x, y)) # add the first point to the list
        
        # for each link in the list
        for i in range(self.num_links):
            link_length = self.link_lengths[i]
            angle = np.sum(self.joint_angles[:i+1])
            x_end = x + link_length * np.cos(angle)
            y_end = y + link_length * np.sin(angle)
            points.append((x_end, y_end))
            x = x_end
            y = y_end
        return points

    def set_joint_angles(self, angles):
        print("her")
        self.joint_angles = angles

    def draw_configuration_space(self):
        # Draw the robot arm configuration
        plt.figure()
        ax = plt.axes()

        for i in range(self.num_links):
            x = np.cumsum([0] + [self.link_lengths[j] * np.cos(np.sum(self.joint_angles[:j+1])) for j in range(i)])
            y = np.cumsum([0] + [self.link_lengths[j] * np.sin(np.sum(self.joint_angles[:j+1])) for j in range(i)])

            ax.plot(x, y, marker='o')

        plt.title('Robot Arm Configuration')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.show()

    # a function to draw the actual robot arm with different line colors and accurate angles and lengths, scaled accordingly
    def draw_robot_arm(self):
        plt.figure()
        ax = plt.axes()

        x = 0  # Start at the base along the X-axis
        y = 0  # Start at the base along the Y-axis
        print(self.joint_angles)

        # for each robot arm link
        for i in range(self.num_links):
            # get the length and base angle of that link
            link_length = self.link_lengths[i]
            # set the angle to the sum of all previous angles
            angle = np.sum(self.joint_angles[:i+1])

            # Calculate the end point of the current link given that x and y are the start point
            x_end = x + link_length * np.cos(angle)
            y_end = y + link_length * np.sin(angle)

            # plot a line from x to x_end and y to y_end
            ax.plot([x, x_end], [y, y_end], marker='o')

            # update x and y to be the end point of the current link
            x = x_end
            y = y_end


        plt.title('Robot Arm Diagram')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axis('equal')
        plt.grid(True)
        plt.show()


    def check_collision(self, obstacles):
        # Check if the robot arm configuration collides with any obstacles
        arm_polygons = self.get_arm_polygons()

        for obstacle in obstacles:
            if arm_polygons.intersects(obstacle):
                return True  # Collision detected

        return False  # No collision

    def get_arm_polygons(self):
        # Generate polygons representing the links of the robot arm
        polygons = []

        for i in range(self.num_links):
            link_polygon = self.get_link_polygon(i)
            polygons.append(link_polygon)

        return affinity.rotate(Polygon(), -self.joint_angles[0])

    def get_link_polygon(self, link_index):
        # Generate a polygon representing a single link of the robot arm
        link_length = self.link_lengths[link_index]

        x = np.cumsum([0] + [link_length * np.cos(np.sum(self.joint_angles[:link_index+1]))])
        y = np.cumsum([0] + [link_length * np.sin(np.sum(self.joint_angles[:link_index+1]))])

        link_polygon = Polygon([(xi, yi) for xi, yi in zip(x, y)])
        return link_polygon

# Example usage:
num_links = 2
link_lengths = [1, 1]  # Example link lengths
robot = Robot(num_links, link_lengths)

# Set joint angles for testing
joint_angles_test = np.radians([30, 30])
robot.set_joint_angles(joint_angles_test)

# Draw the robot configuration
robot.draw_robot_arm()

# # Check collision with an obstacle
# obstacle_polygon = Point(2, 1).buffer(0.5)  # Example obstacle
# obstacles = [obstacle_polygon]

# if robot.check_collision(obstacles):
    # print("Collision detected!")
# else:
    # print("No collision.")
