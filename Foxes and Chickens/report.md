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

To test the `get_successors` function, I called it on a series of states and calculated the valid successors on my own to compare, and everything looked good. 

Note** I saw mention of the `goal_state` function in the notes, but at least for the purposes of the type of games we would use this algorithm for, I figured that this was unecessary and that simply comparing the `search_problem.goal_state` to the current node's state would suffice, since it can be done directly (assuming consistent state representations).

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

To test the breadth-first search, I used the game state tree created in the introduction. Everything looked good, so from that point I inserted a few print statements to check the state of the queue and see which state was currently being examined at each step. I first checked this to make sure that the states made sense-- i.e. that they were all legal states coming from valid successors. I already tested the successor methods before, but I wanted to double check. Then, I traced through the rest of the path returned and even used my `get_successors` method on its own to ensure that the states were being visited correctly, and that no invalid states were visited. 

I also googled a shortest-path solution to the `(3, 3, 1)` problem and it matched my BFS solution perfectly. 

## Memoizing Depth-First Search Discussion: 

Although I did not implement the memoizing DFS, I discuss its time and space comlexities below. In the case of both the memoizing DFS and the BFS, the space complexity is equal to the time complexity. However, this value differs between the two: for BFS, it is O(min(n, b^d)), while for memoizing DFS, it is O(min(n, b^m)), where `n` is the state space size, `b` is the branching factor, `d` is the depth of the goal, and `m` is the length of the longest path. Accordingly, memoizing DFS doesn't save much space-- at the very most, the depth `d` of the goal will be equal to the longest path `m`, so the space complexity of memoizing DFS will be greater than or equal to the space complexity of BFS at the worst.

## Path-Checking Depth-First Search

### Implementation

Although I considered writing a helper functin for the `dfs_search`, I decided to go with just one function to call recursively for simplicity. First is initializing the start_node: this is obvious. 

From here, I though of the three base cases: reaching the `depth_limit`, reaching a leaf, or finding the `goal_state`. Handling them is slightly complicated, because we want to traverse back up the tree if the goal_state is found, but continue searching if a leaf is reached or the depth limit is reached. 

Accordingly, I handle the `goal_state` base case just by adding the `goal_state` node to the path, and then returning the solution before any further recursive calls are made. This instantly passes the solution with the path up the recursive call stack and returns it. 

Since we handle the leaf and depth limit cases the same- by continuing the search laterally but not going any deeper- I handled them in the same way. To do this, I first retrieve the successors of the node (storing them to use later if they exist). Then, I check if either the length of the `successors` list returned from the `get_successors` is empty or if the depth has been reached to satisfy both cases. If either are true, I return the existing solution. This is handled by the recursive case. 

For the recursive case where we assume the node is not the goal state node, it has successors, and we are free to continue searching deeper, I iterate through each of the successors. To avoid revisits, I check if it is in the solution path already. Then, I remember the current length of the path, and then call `dfs_search` recursively, passing it the successor to visit it and update the solution. Since I am just passing this one solution object down the tree, I know its path length will be increased if the node we passed it is the goal node or has successors, so I then check to see if the length has changed. 

If the length of the solution's path has not changed, we know it is a leaf or we are at the depth limit, so we continue to the next successor in the for loop. Otherwise, we know that the recursive calls have already been made, so any updates to our solution will be executed at this point, so we just return it. 

Finally, in the case that successors exist, but none of them return valid paths (which means no return is executed), we pop the most recently added node from the list, returning the initial solution (which will passed back up the stack until there are no more calls left or a longer path is found)

Pseudocode is as follows: 
```
if no node given, initialize the start_node and solution
base case 1: if the goal is found
    add it to the path and return the solution
base case 2: if a leaf is reached or the depth limit is reached
    return the existing solution to continue the search laterally
recursive case: 
for each successors
    call dfs to update the solution 
    if the length of solution doesn't change
        go to the next successor
    if it does
        return it
if no successors returned
    pop the current node and return the current solution
```

### Testing 

In order to test the depth first search, I once again used print-statements to verify that the tree was being traversed correctly. At each step, I printed the current node being visited, it's successors, if any, and the current path. This allowed me to draw an accurate game tree as it was constructed by the algorithm on paper, and run back through it to make sure that each call was visiting the correct node. I did this for the `(3, 3, 1)` scenario tree, and checked every step. 

I also tested this using my own pre-programmed `depth-limit`, which allowed me to make sure that it was working properly. 

## Iterative Deepening Search

### Implementation

Lastly, I implemented the IDS simply by initializing variables to store the path and the number of nodes visited, and then iteratively calling `dfs_search` and incrementing the depth limit each time till a path is found. Pseudo is as follows: 

```
remember path and nodes visited
loop through indexes 1 through depth limit
    increment the number of nodes visited after each search
    if a path is found
        stop iteration
return the solution, which will have an empty path if not found
```
This method results in very low memory usage (it only has to store the current path using path checking dfs, and we guarantee this will be the shortest path), but very high runtime (we search each node i-d times, where i is the current max depth, and d is the depth of the node.)

### Testing

I tested the ids by (once again) using print statements. This time, I embedded them in both the dfs and ids algorithms, that way I could ensure that both were working together in tandem. For example, I had the ids algorithm print out the dfs response after each iteration, allowing me to check that the path and depth was calculated correctly. I also tested the entire algorithm on the test problems I used for the others, ensuring that the `path` and `nodes visited` were working correctly in all scenarios. This all looked good to me-- I didn't trace every step of the tree like in the dfs before, but after all, it was the same algorithm that I did test. 

As for which search method I would use on a graph, I would probably implement path checking dfs in tandem with the ids algorithm. If you're using the ids, your priority obviously isn't runtime-- it's saving memory. Using memoization would be counterintuitive in this scenario, since (as discussed above), we can assume it will use as much as or more space than the path checking dfs (usually, it will use much more). 

In comparison with the dfs agorithms, I would only use ids if memory was my top priority and runtime didn't really matter. Path checking dfs is the second most advantageous for memory, while memoizing is least advantageous.

## Discussion: Lossy Chickens and Foxes

If a few chickens were willing to be eaten for the greater good, we'd have to use another variable in the state to represent the number of chickens left that are willing to be eaten. I'd just add this to the tuple: `(foxes, chickens, boats, sacrificial chickens)`. I'd then store the original amount of chickens willing to be eaten in the `start_state`. This wouldn't change the actions for a problem if our boat only holds two animals at any time, but it would definitely change which states are valid. For example, the state, `(2, 1, 1)` was not valid before, but the state `(2, 1, 1, 2)` is certainly valid despite having more foxes than chickens on one side, since that chicken would be willing to be eaten. Now, possible solutions would be `(f)(c)(b)(e)`, including legal states. Legal states now must satisfy the conditin `c <= f - e` on both sides. 

## Extra Credit: 

Obviously just looking at states for these problems gets a bit messy... so visualization is helpful. In my `foxes.py`, find the function `visualize_solution` that taxes a `search_problem` and a `path`, and visualizes it in console output. This isn't super fancy, but note the following: 
- The boat will be displayed separately from the foxes and chickens, with a `B`. 
- Foxes and chickens will be displayed with `C` and `B`, on their respective sides
- The river is marked with a `|`
- Each state is separated by the adequate number of `-` for each problem, given its size. 