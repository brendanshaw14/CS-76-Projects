import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
from shapely import affinity

class Robot:
    def __init__(self, angles, link_lengths):
        self.angles = angles
        self.link_lengths = link_lengths
        self.points = self.get_points()

    def __str__(self):
        return f'Robot: {self.angles}'

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
    def draw_robot_arm(self, obstacles):
        plt.figure()

        # draw the obstacles, if they exist
        if obstacles:
            for obstacle in obstacles:
                plt.plot(*obstacle.exterior.xy, color='red', linewidth=2, linestyle='-', alpha=0.5)
                plt.fill(*obstacle.exterior.xy, color='gray', alpha=0.5)

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
        # for each link in the robot arm
        for i in range(len(self.link_lengths)):
            # get the start and end points of that link
            start_point = self.points[i]
            end_point = self.points[i+1]

            # for each obstacle
            for obstacle in obstacles:
                # if the start or end point is inside the obstacle
                if obstacle.contains(Point(start_point)) or obstacle.contains(Point(end_point)):
                    return True

                # if the obstacle intersects the line between the start and end points
                if obstacle.intersects(LineString([start_point, end_point])):
                    return True

        # if no collision is detected, return false
        return False



if __name__ == '__main__':
    num_links = 2
    link_lengths = [1, 1]  # Example link lengths
    joint_angles = np.radians([55, 135])
    print(joint_angles)

    # make obstacle
    obstacle_polygon = Point(0.6, 0.6)  # Example obstacle

    # make an example square that will collide with the above line
    obstacle_polygon = Polygon([(0.5, 0.5), (0.5, 0.7), (0.3, 0.7), (0.3, 0.5)])
    obstacles = [obstacle_polygon]
    robot = Robot(joint_angles, link_lengths)

    # Draw the robot configuration
    robot.draw_robot_arm(obstacles)
    if robot.check_collision(obstacles):
        print("Collision detected!")
    else:
        print("No collision.")
