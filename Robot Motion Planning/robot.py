import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from shapely import affinity

class Robot:
    def __init__(self, angles, link_lengths):
        self.angles = angles
        self.link_lengths = link_lengths
        self.points = self.get_points()

    # initialize self.points to be a list of points that represent the robot arm using the angles and lengths
    def get_points(self):
        # initialize empty list, x and y to be 0
        points = []
        x, y = 0, 0 
        points.append((x, y)) # add the first point to the list
        
        # for each link in the list
        for i in range(len(self.link_lengths)):
            link_length = self.link_lengths[i]
            angle = np.sum(self.angles[:i+1])
            x_end = x + link_length * np.cos(angle)
            y_end = y + link_length * np.sin(angle)
            points.append((x_end, y_end))
            x = x_end
            y = y_end
        return points

    # a function to draw the actual robot arm with different line colors and accurate angles and lengths, scaled accordingly
    def draw_robot_arm(self):
        plt.figure()
        ax = plt.axes()

        # for each robot arm link
        for i in range(len(self.link_lengths)):
            # get the length and base angle of that link
            start_point = self.points[i]
            end_point = self.points[i+1]
            print(start_point, end_point)

            # plot a line from start_point to end_point
            plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], linewidth=2, marker='o')

        plt.title('Robot Arm Diagram')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

    # function 

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

        for i in range(len(self.link_lengths)):
            link_polygon = self.get_link_polygon(i)
            polygons.append(link_polygon)

        return affinity.rotate(Polygon(), -self.angles[0])

    def get_link_polygon(self, link_index):
        # Generate a polygon representing a single link of the robot arm
        link_length = self.link_lengths[link_index]

        x = np.cumsum([0] + [link_length * np.cos(np.sum(self.angles[:link_index+1]))])
        y = np.cumsum([0] + [link_length * np.sin(np.sum(self.angles[:link_index+1]))])

        link_polygon = Polygon([(xi, yi) for xi, yi in zip(x, y)])
        return link_polygon

if __name__ == '__main__':
    num_links = 2
    link_lengths = [1, 1]  # Example link lengths
    joint_angles = np.radians([45, 135])

    # make obstacle
    obstacle_polygon = Point(0.6, 0.6)  # Example obstacle
    obstacles = [obstacle_polygon]
    robot = Robot(joint_angles, link_lengths)

    # Draw the robot configuration
    robot.draw_robot_arm()
    if robot.check_collision(obstacles):
        print("Collision detected!")
    else:
        print("No collision.")
