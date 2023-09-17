# Foxes and Chickens Report

## Initial Discussion

To begin, I decided to use the game representation mentioned in the assignment using a tuple containing three values to represent the number of foxes, chickens, and boats on the left side of the river, respectively (for example, `(3, 3, 1)` represents the initial game state). To represent actions, I used a similar system, using another tuple to represent the change in foxes, chickens, and boats on a given side (for example, `(-2, 0, -1)` means sending two foxes to the opposite side). 

To begin the search algorithms, I had to think about the possible game states and actions, as well as which ones are legal and illegal. Using the original scenario with 3 foxes, 3 chicken, and two spots in the boat, there are 0, 1, 2, or 3 foxes and chickens on the left side, and either 1 boat or no boat (0 boats). That yields `4*4*2=32` possible combinations-- though many of these are not valid game states. For a game state to be legal, both sides must have either as many or more chickens than foxes, or no chickens at all. It's also worth noting that some of these states are impossible to achieve, such as the state `(3, 3, 0)`: the boat can't get accross the river without animals in it. As for actions, the only rule is that the boat may only carry up to two animals at one time, and must carry at least one animal. Therefore, our options are: move two chickens, move two foxes, move one chicken and one fox, move one fox, or move one chicken-- five actions in total. 

These rules yield the following game tree (up to a degree of 2). I've included only valid states (where foxes and chickens are both greater than 0), and illegal states (where there are more foxes than chickens one one side) are marked with a red line through them. Also note that the original game state appears as a successor multiple times-- we will have to ensure this is accounted for later. 

![Alt text](<images/game tree.svg>)

## Retrieving Successors and State Validation

Before implementing the different search algorithms, I had to design methods to retrieve the valid successor states for a given state. To break down the task, I decided to break things down as simply as possible. 

The `get_successors` function takes a `state`, so I had to find a way to apply all of the possible actions to the state and then only return the valid successor states. The main challenge with this was the distinction between the left and right sides of the river, because the action will be applied differently depending on which way the boat is traveling. 

To handle this, I defined the list of actions (`[(-2, 0, -1), (-1, 0, -1), (-1, -1, -1), (0, -1, -1), (0, -2, -1)]`) as a class attribute, and then used an if statement to determine whether the boat is on the left or right side and apply the actions accordingly. If the boat is on the left, we can just add the action values to the state values to calculate the resulting state. If it is on the right, we can just subtract the values-- subtracting from the right side of the river adds to the left, and action values are negative.  

Then, I wrote a helper function `is_valid_state` to verify the legality of the states. The two objectives were to verify that the fox and chicken values were within the possible ranges, and that there were not more foxes than chickens on either side. To do this, I first verify that the fox and chicken values are at least 0. This is because applying the an action that removes non-existent animals from the left side (ex., applying `(-2, 0, -1)` to the game state `(1, 1, 1)`) results in a negative number (`(-1, 1, 0)`). Similarly, we also must verify that the fox and chicken values aren't greater than the starting state values, because moving non-existent animals from the right side (ex., applying `(2, 0, 1)` to the game state `(2, 0, 0)` results in an invalid state because there can be at most one fox on the right side-- so moving two back over to the left would result in the state `(4, 0, 1)`-- which isn't possible).

In total, the `get_successors` function works as follows: 
```
make a list of successors
if the boat is on the left side:
    for each action:
        add each value of the action (which contain negative numbers representing how many foxes and chickens are removed from that side) to the current state's corresponding value
        if the resulting state is valid, add it to the list 
else (the boat is on the right side):
    for each action:
        subtract each value of the action (which contain negative numbers representing how many foxes and chickens are removed from that side) to the current state's corresponding value
        if the resulting state is valid, add it to the list 
return the list
```

## Breadth-First Search 

### Implementation
To implement the breadth-first search, I begin by initializing a `deque` with just the `start_state` node. I use Python's `set` to keep track of nodes I visit to avoid revisits and infinite loops in `visited_states`. I add the `start_state` immediately, as to avoid any loops that would occur from revisiting the initial state. I also initialize the `SearchSolution` so that a `SearchSolution` object with an empty path will be returned if the goal is not found. 

To begin the search itself, I use the methods discussed in class: 

```
while there are nodes in the queue: 
    pop the item from the left, increment num_nodes_visited
    if this is the goal state:
        backchain, return the solution
    else:
        get the successors for the state
        add any successors not in the visited set to the queue
```

As suggested by Prof. Balcom, I used a helper function `backchain` for backchaining. The function takes only the goal `SearchNode` as a parameter, because we can rely on the `parent` states stored in each node to trace our path back to the `start_state`: which has no parent value. 

The backchaining goes as follows: 
```
make an empty list for the path
set the current node to be the input goal node
while the current node has a parent (meaning it is not the start_state):
    add the current_node to the path
    update the current node to be its parent
reverse the path to order it starting from the start_state
return the path
```

### Testing