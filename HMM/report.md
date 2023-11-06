# HMM Mazeworld Report

The principal objective of this lab was to create an HMM (hidden markov model) to represent the mazeworld problem, with a few twists. In this problem, we consider a robot navigating a maze consisting of empty squares, each painted with one of four colors: red, green, yellow, or blue. The robot is initially placed in an unknown location within the maze. At each time step, the robot can move in one of four directions: North, South, East, or West. However, if there is a wall in the chosen direction, the robot remains in its current location, but this still counts as a turn.

The robot is equipped with a sensor pointing downwards, capable of detecting the color of the floor it is currently on. However, the sensor is not perfect. If the robot is on a blue square, the sensor will correctly indicate the color "b" with a probability of 0.88. However, there is a chance of error, leading to readings of "r" (red), "g" (green), or "y" (yellow) with probabilities of 0.04 each. The sensor's behavior is symmetric for squares of other colors.

The robot's initial location is unknown, and it chooses its movements randomly. Specifically, it selects a direction uniformly at random. If the chosen direction is blocked by a wall, the robot remains stationary, still using up a turn.

The goal is for the robot to determine its location within the maze based on the sequence of sensor readings it receives after each attempted move. The robot starts with an equal belief that it could be in any of the 16 possible locations, resulting in an initial distribution of (.0625, .0625, .0625, ..., .0625). As it receives sensor readings and makes moves, it updates its beliefs about its location, taking into account both the sensor information and the possible movements.

An HMM is ideal for this problem because it allows us to calculate the probability of the robot being in each location in the maze (the hidden states) based on the sequence of sensor readings it receives (evidence).

## General Process of the HMM: 

The HMM works by maintaining a probabilistic distribution of the robot's possible locations in the maze. At each step, this distribution is used in tandem with the probability of transitioning from each location in the maze to the other locations to predict the robot's next location. Then, a sensor reading is obtained after movement, which we use to update the probability distribution.

1. **Initialization:** The HMM starts with an initialization step, where the maze layout is represented, and the robot's initial beliefs about its location are established. In this problem, this entailed initializing the maze to store colors randomly assigned to each floor space, and initializing the robot's belief distribution to be uniform across all possible locations.

2. **Probabilistic Movement:** The robot's movement is modeled probabilistically. At each step, the user can choose a direction (North, South, East, or West). Since the model is unaware of which direction the user moves the robot, we assume there is equal likelihood that the robot will move in each direction. However, obstacles such as walls restrict its actual movement. The transition probabilities in the HMM capture these movement constraints. We store these in a matrix, where each row represents a spot in the maze, and each column represents the probability of transitioning from that row's corresponding spot to the column's corresponding spot. These probabilities are computed based on the layout of the maze, allowing the model to predict the robot's possible locations after a move. 

3. **Sensor Readings:** The robot's sensor provides color information about its current location. Due to sensor inaccuracies, the received color might not always match the actual location color. The sensor readings are used to update the robot's beliefs. If the sensor detects a specific color, the probabilities of the robot being in locations with that color increase, reflecting the likelihood of its true position.

4. **Prediction and Update:** The core of the HMM involves two key steps: prediction and update. In the prediction step, the model estimates the robot's probable locations after movement, considering the transition probabilities. Following movement, the sensor readings trigger the update step. Here, the probabilities are adjusted based on the observed color, refining the robot's belief about its location.

5. **Normalization:** To maintain the probabilistic nature of the distribution, the probabilities are normalized after each update step. Normalization ensures that the sum of probabilities equals 1, providing a consistent representation of the robot's beliefs across all possible locations.


## Implementation 

### Maze.py

To begin the implementation, I copied the `Maze.py` class from the mazeworld problem into the HMM directory. The use of this class is very similar to the mazeworld problem, but I did add a few components. 

1. In the constructor of the `Maze` class, I added a `color` attribute to each floor space by creating a dictionary that associates each floor space on the maze with a color. This is used to determine the color of the robot's current location, which is used in the sensor update step.

```
# assign colors to floor spaces
        self.colors_map = {}
        for y in range(self.height):
            for x in range(self.width):
                # make sure the space is a floor 
                if self.is_floor(x, y): 
                    # randomly choose a color out of red, yellow, green, and blue:
                    self.colors_map[(x, y)] = random.choice("rygb")
```

2. Accordingly, I also added a `get_color` method to the `Maze` class, which returns the color of the floor space at the given coordinates using the dictionary in the constructor. This is used to determine the color of the robot's current location, which is used in the sensor update step.
```
def get_color(self, x, y):
    return self.colors_map[(x, y)]
```

3. For debugging purposes, I also wrote a new method to return the string of the colored maze. This is used to print the maze with the colors of each floor space, which is useful for debugging and visualizing the robot's movements.

### mazeHMM.py

The `mazeHMM.py` file contains the `MazeHMM` class, which is used to represent the HMM for the mazeworld problem. 

The constructor of the `MazeHMM` class takes in a `Maze` object, which is used to initialize the maze layout and the robot's initial belief distribution. The maze layout is used to initialize the transition probabilities, and the robot's initial belief distribution is used to initialize the probability distribution. 

The instance variables `self.distribution` and `self.transition_probabilities` are used to store the state distribution and transition probabilities, respectively. Information about the maze is stored in the maze object `self.Maze`

First, I discuss the main loop used to run this model:

`def run(self)`:
The main method used to run the program here is the `run` method. This method implements the general process of the HMM described above. This function requests user input from the command line, prints the maze, probability distributions, sensor readings, and robot path to the command line. The function runs this in a loop that can be exited by the user at command line with the key `q`. At each iteration, the model updates the probability distribution using The user inputs a key into the command line, which can be w, a, s, or d to move the robot, or q to quit. Then, the model uses this input to move the robot in the maze, updating its location in the `Maze` object. After this, the emission reading from the color sensor can be obtained. At this point, we can update the probability distribution using the sensor reading. Finally, the model prints the maze, probability distributions, sensor readings, and robot path to the command line, and waits for the next input. 
Pseudo: 
```
def run(self): 
    print start state
    initialize the loop
        use the current state to predict the next state with transition probabilities
        get the user's next move and update the robot's location with it 
        get the sensor's reading based on the new location
        udpate the distribution 
        normalize it 
        print the updates
```

Before this loop can be run though, we must initialize the probability distribution, as well as the transition probability matrix.

`def initialize_start_distribution(self)`:
This function sets up the initial probabilities for the robot localization problem. It explores the maze, counting the available floor spaces. For each valid floor area, the function assigns a uniform probability, ensuring the robot's starting position remains unknown and equally probable across all possible spots. By dividing 1 by the total number of valid floor spaces, this function establishes a starting belief where the robot could be anywhere in the maze with an equal chance, laying the groundwork for the probabilistic calculations. 

Pseudo: 
```
        # keep track of maze floorspace
        # for each location in the maze
            # if the location is a floor
                # increment floorspace
        # for each location in the maze
            # if the location is a floor, set the numpy matrix at that location to be 1 / (width * height)
```

`def initialize_transition_probabilities(self)`:
This method systematically explores each position in the maze, considering only the valid floor spaces where the robot can move. For every valid spot, the function calculates transition probabilities to neighboring locations. These probabilities are set to 0.25, indicating an equal likelihood of the robot moving in any of the four cardinal directions. If a neighboring spot is a wall, the probability of staying in the current position (represented by the diagonal elements of the transition matrix) is incremented by 0.25. 

Pseudo: 
``` 
def initialize_transition_probabilities(self):
    initialize the actions array
    for each index in the transition probabilities matrix
        get the x and y coordinates of the index
        skip if not a floor
        for each adjacent spot to this index (retrieved from actions):
            get the x and y coordinates of the adjacent spot
            if that spot is a floor:
                calculate the index of this spot in the array
                set the probability of moving there to 0.25
            if that spot is not a floor:
                increment the probability of not moving at all by 0.25 
```

Afterwards, I wrote the methods for the prediction, update, and normalization steps of the HMM. First was the prediction step, which calculates the predicted probability distribution after the move before getting the sensor emission.  

`def predict(self)`:
This method turned out to be pretty simple becasue I figured out how to just use numpy matrix multiplocation to do the prediction step. I just multiply the transition probabilities matrix by the distribution matrix, and then normalize the result to account for the scale factor. This multiplies the probability of transitioning from one state to another by the probability that the robot is in the start state, and adds the resulting probabilities that the robot is in each location. Then, I normalize the result to account for the scale factor.
```
    new_distribution = np.matmul(self.transition_probabilities, self.distribution)
    self.distribution = new_distribution / new_distribution.sum()
```

Now, we have to get the robot's next move from the user. Rather than inputting a set of moves that was precoded, I made it so that the run function awaits user input using the `get_next_location` function:

`def get_next_location(self)`:
If the user inputs a valid move, the robot moves in that direction. This is done by applying the action associated with the movement key, and updating the `Maze` object's `self.robotloc` instance variable, which allows us to accurately use the `get_color` method I added to `Maze.py`. If the user inputs an invalid move, the robot stays in place, and an error message is displaced. If the user inputs q, the program quits. 

Pseudo: (**note**: I did have to add a few other lines to this to make the user interface work correctly, but this is the general logic.)
```
def get_next_location(self):
    define a dictionary associating moves in the form `(dx, dy)` with the keys w, a, s, and d.
    prompt the user to type w, a, s, or d to move the robot
    wait for a valid key input
    update the robot's location
        if the new space is a floor
            move the robot there
        if not a floor:
            do not move the robot
```

Once the robot is moved, we need to get the sensor's next reading to update the model, which I did with `get_sensor_reading`. This function just uses the `self.maze.get_color` method I added to `Maze.py` to get the color of the floor space the robot is currently in. Then, it picks a random number between 0 and 1. If this number is less than the probability of the sensor reading the correct color, we return the correct color. Otherwise, we randomly choose one of the other colors to return. 

This is simple, so here's the actual code: 
```
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
```

Finally, we update and normalize this distribution to account for the sensor reading. First this uses the `update` method. 

`def update(self, sensor_reading)`: Here, we use our knowledge of the color locations in the maze to update the probability. We iterate through the maze, and for each floor space, we check if the sensor reading matches the color of that space. If it does, we multiply the probability of the robot being in that space by 0.88. If it doesn't, we multiply the probability by 0.04. This is because the sensor has an 88% chance of reading the correct color, and a 4% chance of reading any of the other colors. As discussed in class, we then account for the scale factor by normalizing the distribution. 

Pseudo: 
```
def update(self, emission):
    # for each state
        # get the x and y coordinates of the state
        # if the state is a floor
            # get the color of the state
            # if the color of the state matches the sensor's reading
                # multiply the probability distribution by 0.88
            # if the color of the state does not match the sensor's reading
                # multiply the probability distribution by 0.04
    # calculate the total sum of probabilities using NumPy sum function
    # divide the entire array by the total using broadcasting
```

These are all of the main method components I used for the markov model. I did write one more easy helper method though, `def dist_to_string(self)`, which prints the probability distribution in the same dimensions as the maze to make it easier to visualize. This way, at each step, the maze with the actual colors and the maze showing the robot's location are printed with the probability distribution in the same format below them, so you can easily see the distribution's predicted value for the robot's true location. 