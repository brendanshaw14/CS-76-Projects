# HMM Mazeworld Report

Plan: 

- save the input maze
- assign colors to the maze using the maze class
- compute starting probabilities (this will be 1/16)
- print the actual maze out with the robot inside along with the current path
- print the probability distribution (this is equal)
- wait for the user to input a new key for movement
    - 
    - get the robot's new location
        - if the 
    - get the color at that location
    - get the sensor reading based on the probability
    - update the distribution
        - for each square
            - if the color matches that square, multiply by 0.88
            - if it doesn't
- print the updated distribution
- print the robot's actual location in the maze, along with the current path
