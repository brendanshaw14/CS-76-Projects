# Mazeworld Report


## Initial Discussion and A* Algorithm: 

I started by writing the A* algorithm first to see what methods and instance variables I would need to adapt the mazeworld problem to it, as well as the sensorless problem. 

I began with the pseudo-code from the textbook, adapting each step to the problem. Here is my improved pseudocode: 

``` 
Make the start node
initialize solution, visited_cost dictionary, and frontier

while there are items in the frontier: 
    pop the next node from the heap
    increment nodes_visited
    add the current node to the path
    update the maze state    
    if the solution was found: 
        backchain and return
    else, get the successors
    iterate through successors: 
        get the cost of the new node
        if the node was visited but at lower cost, go to the next node
        if it wasn't visited or was visited with a higher cost, add it to the heap with the new cost
return the solution with an empty path if goal wasn't found
```

With this adaptation of the algorithm, I was ready to write the methods within the `MazeworldProblem`. 

### State and Action Representation

The challenge here was that I just wanted to write the problem one time over and make it adaptable to both the single and multi_robot scenarios. The documentation was a bit difficult to read, but after some scanning I realized it would probably be easiest to just store the game state as a tuple `(robot_turn, robot1_x, robot1y, robot2x, robot2y)`, etc. 

This would allow for efficient and easy comparison between states, retrieval of state data, and construction of successor states. 

I used a simple `dx, dy` action representation, with the possible actions being `[(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]`. The only challenge to think about with this was that the (0, 0) action is only for problems with multiple robots-- applying it to a single robot repetitively results in no movement and just an infinite loop. 

### Constructor: 
The constructor holds the following: 
- the `maze` object itself- `self.maze`
- an array of goal locations- `self.goal_locations`
- the number of robots in the maze (this is useful for iteration in `get_successors` and `goal_test`- `self.num_robots`
- the start state- `self.start_state`

This was pretty straightforward. I don't have much else to say on it, besides that I set up the start state by looping through the `maze` object's `robotloc` list to add the robot(s)'s starting coordinates to the state. 

The string method is simple. Just look at it-- it makes sense. 

### Update

I realized in writing the A* search that I needed a way to maintain the robot locations correctly in the `maze` object, or else the `has_robot` method would not work correctly with multiple robots since their locations wouldn't be updated. 

I just wrote a simple update function: 
```
#updates the maze object to store the current location of the robots for accurate is_flooor testing 
    def update(self, state):
        # for each robot
        state = list(state)
        self.maze.robotloc = state[1:]
        return True
```

This just loops through the list of robots and updates the maze opject with their locations based on the current game state. 

### Getting Successors
Pseudocode: 
```
 get which robot's turn it is - this is the first value
    get current robot's x and y
    for each action
        apply the action
            if the new location is a floor and doesn't have a robot in it 
                update which robot's turn it is
                update the robot's location
    determine whether or not to include just switching the turn as an action
        increment which robots turn it is or reset it to 0 if it is the first one again
```

In summary, I just apply each action to whichever robot's turn it is. If that location is free, I add it to the list of successors. After that, add changing the robot's turn as an action, if possible. 

### Goal Testing

Based on what was written in the assignment, I originally assumed that it deosn't matter which location each robot is in, so long as every robot is in the goal location, the goal state is reached.
Therefore, I first wrote the goal state as follows: 

Pseudocode: 
```
for each robot: 
    get its index from the state
    if that index is not a goal location: 
        return false
    else: 
        remove that location from the locations list, go to the next robot
if false isn't returned by now, all robots are in a goal location: return true
```

Then, I realized that we were probably supposed to make sure each robot was in a set location, so I implemented this too. See `assigned_manhattan_heuristic`. 


### Get Cost

I added this function only after beginning the blind robots in the maze problem, in which I realized I had to have a way to retrive the cost of getting from one state to another in all scenarios. Previously, I had just hard-coded it, but that wasn't working with the sensorless problem because of the state storage being different, so I just made both problems use a get_cost function that takes two states. 

For the sensorless problem, it just returns 1 every time-- there isn't a move that costs less than 1. For the normal problem, I return 1 if one of the robots moved, and 0 if they switched turns and didn't move. 

### Manhattan Heuristic 

I used a manhattan distance heuristic like the one we discussed in class for the single and multi_robot problem. I wrote two versions of this: the first one is simple and monotonic: it just iterates through each robot, finding the nearst goal, and adding the distance to that goal to the total distance, returning that number. 

If there's one robot, it will just find the nearest goal to that robot and return it. If there are multiple robots and all are closest to the same goal, it will return the sum of that distance for every robot. This is sometimes inaccurate, but it is monotonic and will always return a shortest path. 

This is why I wrote the modified version too though. 

## Sensorless Problem: 

I made the sensorless problem a very simple adaptaion of the original `MazeworldProblem`. The setup is the same, except we don't keep track of the robots' locations. Rather, we initiate the start state with every possible location, and then try to narrow it down until we are certain of where the robot is. 

To do this, I used `get_successors` function that just applies every single action to every belief state. Then the resulting outcomes are added to the new belief set, but since duplicates are prevented and we assume that the maze has walls (so sometimes the robot cannot move), we will reduce the size of the belief state. 

The heuristic simply returns the size of the state set, so we aim to reduce the size until we know the robot's location. 

This is the goal_state: we just test to see if the state set size is 1 yet. 

This all worked well: see the tests. 


## Discussion Questions: 

1. If there are k robots, how would you represent the state of the system? Hint – how many numbers are needed to exactly reconstruct the locations of all the robots, if we somehow forgot where all of the robots were? Further hint. Do you need to know anything else to determine exactly what actions are available from this state?

- We just need the location of each robot (an x and a y), and then which robot's turn it is. So, that is `2 * num_robots + 1` values. To determine available actions, we need to know if the surrounding spaces are floor or wall tiles, which are stored in the `maze object`. This is why we update the maze. 

2. Give an upper bound on the number of states in the system, in terms of n and k.
- If there are `k` robots in an `n * n` maze, then there are `n^2` possible locations for a given robot. However, if a robot is in one of the locations, this isn't availble, so it is more like `n^2 choose k` possible state spaces, at maximum. 

3. Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.
- This means that the available number of total tiles is `n^2-w`, which gives is `n^2-w` choose k possible state spaces. 

4. If there are not many walls, n is large (say 100x100), and several robots (say 10), do you expect a straightforwards breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?

5. Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.

- A useful, monotic heuristic for this search space is just finding the sum of the distance between each robot and it's goal. If we don't assign robots to specific goals, we can use a less specific heuristic that just sums the distance from each robot to the nearest goal- which will never result in an overestimation. 

6. (See `astart_test.py`)

7. Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?

- The 8 puzzle is functionally a 9x9 maze with 8 robots and no walls-- so it's basically just another mazeworld problem. If we assume each robot has a specific goal location, use the appropriate goal test, and ensure that the manhattan distance for each robot to its goal is summed for the heuristic, the algorithm can solve this easily. 

8. The state space of the 8-puzzle is made of two disjoint sets. Describe how you would modify your program to prove this. (You do not have to implement this.)

This modification would necesitate the useage of a heuristic for each disjoint state. We would have to find a way to add the number of actions that affect each state and only that state. Since this would exclude moves shared between both states, it would certainly result in an underestimation and therefore be consistent. 
