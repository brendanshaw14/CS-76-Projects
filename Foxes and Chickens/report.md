# Foxes and Chickens Report

## Initial Discussion

To begin, I decided to use the game representation mentioned in the assignment using a tuple containing three values to represent the number of foxes, chickens, and boats on the left side of the river, respectively (for example, `(3, 3, 1)` represents the initial game state). To represent actions, I used a similar system, using another tuple to represent the change in foxes, chickens, and boats on a given side (for example, `(-2, 0, -1)` means sending two foxes to the opposite side). 

To begin the search algorithms, I had to think about the possible game states and actions, as well as which ones are legal and illegal. Using the original scenario with 3 foxes, 3 chicken, and two spots in the boat, there are 0, 1, 2, or 3 foxes and chickens on the left side, and either 1 boat or no boat (0 boats). That yields `4*4*2=32` possible combinations-- though many of these are not valid game states. For a game state to be legal, both sides must have either as many or more chickens than foxes, or no chickens at all. As for actions, the only rule is that the boat may only carry up to two animals at one time, and must carry at least one animal. Therefore, we can only move two chickens, two foxes, one chicken and one fox, one fox, or one chicken-- five actions in total. It's worth noting that some of these states are also impossible to achieve, such as the state `(3, 3, 0)`: the boat can't get accross the river without animals in it. 

These rules yield the following game tree (up to a degree of 2). 

![Alt text](<images/game tree.svg>)

## Retrieving Successors and State Validation

Before implementing the different search algorithms, I had to design methods to retrieve the valid successor states for a given state. To break down the task, I decided to break things down as simply as possible. 

The `get_successors` function takes a `state`, so I had to find a way to apply all of the possible actions to the state and then only return the valid successor states. The main challenge with this was the distinction between the left and right sides of the river, because the action will be applied differently depending on which way the boat is traveling. 

To handle this, I defined the list of actions (`[(-2, 0, -1), (-1, 0, -1), (-1, -1, -1), (0, -1, -1), (0, -2, -1)]`) as a class attribute, and then used an if statement to determine whether the boat is on the left or right side and apply the actions accordingly. If the boat is on the left, we can just add the action values to the state values to calculate the resulting state. If it is on the right, we can just subtract the values-- subtracting from the right side of the river adds to the left, and action values are negative.  

Then, I wrote a function `is_valid_state` to verify the legality of the states. The two objectives were to verify that the fox and chicken values were within the possible ranges and that there were not more foxes than chickens on either side. To do this, I first check 
## Breadth-First Search 

