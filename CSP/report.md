# CSP Report

This report discusses the design, implementation, and testing processes of the CSP project.

For information on how to run the code and view outputs, see `README.md`. 

The layout of this report is as follows: 
- General structure and problem approach
- Backtracking algorithm 
- Inference and related algorithms
- Map coloring problem design and implementation
- Circuit board problem design and implementation
- Heuristic implementation
- Testing
- Extra credit explanation

## General structure

Since we were not given any provided code, I began by deciding what information to store in which class. This was a little bit difficult at first, but I ultimately decided to have two components to the problem representation and solving: the `CSP.py` class for solving logic and then a class to represent each problem. I tried to store as much information and problem logic in the problem classes as possible, becuase this allows for more flexibility specific to each problem. 

Don't pay too much attention to the `GenericCSP.py`: it contains some generic structure with function headers. This was just for me to organize more easily and make a new problem class more easily if need be using this scaffold. 

## Backtracking algorithm 

I started with the basic backtracking algorithm before I even began coding the representation for the map coloring problem or circuitboard problems. My intention was to have a decent idea of what information I would need to extract from the problem at different points in the algorithm and then build the class around a representation that would allow for simple generic representation. This is what I began with for the backtracking algorithm: 

```
If the assignment is complete, return it as a solution.
Select an unassigned variable using variable selection heuristics.
Loop through the values in the domain of the selected variable
    Check if the assignment of the value to the variable is consistent with the rest of the assignment.
        If so, assign the value to the variable.
        Call backtrack recursively 
        If a solution is found, return it.
        If no solution is found, undo the assignment.
If no solution is found, return None to indicate failure.
```

I began with these methods to do so: (see `GenericCSP.py`, as well as any of the other problem classes for these)
- `is_assignment_complete` - returns true if every variable has been assigned successfully 
- `get_variables` - returns a list of the problem's variables
- `get_domains` - if no variable is specified, return the domains dictionary. Otherwise, return a list representing the domain of that variable.
- `get_constraints`
- `choose_next_variable`
- `is_consistent`

This made things pretty easy. Since all of these methods have some type of problem specific logic except for `is_assignment_complete` (which I ended up putting in the `CSP` solver class), I just implemented them within their specific problems. There are some similarities from problem to problem and I had to keep track of what each method should return, so I created the `GenericCSP.py` class as a general representation for easier adaptation to each problem. This way, I never rely on direct access to instance variables, and just use a few common methods for each step of the problem logic. 

Most notably, this system eliminates the need for any type of integer conversion for the data representation-- all of the data is compared through the problem class methods, so we never have to convert anything. This made the entire project much easier to debug and just took some work off my hands that would've come with this transfer. 

At this point, I began the implementation of the map coloring and circuitboard problems, but for the sake of readability, I discuss those both after the implementation of MAC3 inference. 

## Inference

Implementing inference was by far the most difficult part of this assignment. The underlying idea behind this is that, at each step (assignment) within the backtracking algorithm, we use that step to recursively prune the domains of unassigned variables using arc consistency. We do this by adding all of the arcs from the neighbors of the currently assigned variable to the currently assigned variable to the queue. Then, we enforce arc consistency between those neighbors and the variable-- that is, we ensure that each value of the neighbors domain can be satisfied by the value of the assigned variable, pruning its domain if necessary. 

However, if we prune the domain of one of the neighbors of our assigned variable, that will in turn affect the possible values of the other unassigned variables. For example, if we assign one variable to `r`, then we know that the domain of its neighbor is now `[g, b]`. If we prune the domain of that neighbor, we must now ensure that all of the neighbor's neighbors will be consistent with at least one value in the original neighbor's domain. 

In the map coloring problem, this doesn't have much effect, becuase knowing that the domain of a variable is reduced to `[g, b]` doesn't tell us anything-- its subsequent neighbors could be red in either case, blue if the original neigbor is green, or green if the original neighbor is blue. 

This has a much greater effect on other problems though (like the circuitboard problem), and can sometimes even solve them outright.

I designed the algorithm according to the above logic with help from the textbook: we do backtracking normally, but at at each new assignment, we prune the domains of the remaining variables to reduce search time. 

What if the inference algorithm finds that this assignment leads to no solution though? Of course, we backtrack, but we have to be able to revert to the old, un-pruned domains. Accordingly, we must maintain both the pruned domain and the original domain, which I did by using python's `deepcopy` method to create a version of the domains dictionary that would allow me to change it without affecting the original copy. That way, if a dead end is encountered, we can just remove the most recent assignment and carry on with the normal path. 

Below are detailed explanations and implementation notes for `backtrack`, `MAC3`, and `Revise` (the MAC helper function). Of course, inference also meant that I needed some new methods within the problem class, which are explained below. 

### Backtracking: 

Notice that these key differences to the original backtracking algorithm: 
- the initial call to the function fetches the domain of every variable and stores it in the `domains` dictionary.
- the domains dictionary is passed on to every call of the function, allowing domain inferences to be utilized
- the instance variable `inference` allows us to toggle inference: if true, after assigning a variable, we enforce arc consistency by passing the domain to `mac3`. Notice that we make a deepcopy of the domain before passing it. 
```
def backtrack(self, domains=None):  
    if this is the first call, set the domains to all possible values
    If the assignment is complete, return it as a solution.
    Select an unassigned variable using variable selection heuristics.
    Loop through the values in the domain of the selected variable
        Check if the assignment of the value to the variable is consistent with the rest of the assignment.
            Assign the value to the variable.
            If inference is enabled: Recursively attempt to complete the assignment.
                copy the domain for the recursive calls
                edit the domain of the assigned variable
                call mac3 to edit domain
                if these are all consistent, recursively call backtrack again
                else, set the result to none
            if inference isn't enabled, call backtrack recursively again with the same domain
            If a solution is found, return it.
            If no solution is found, undo the assignment.
```
### MAC-3:

Some other key implementation notes: 
- the queue's order doesn't matter in this case, so we just use a list and name it `queue`. This is effectively a set, but there should not be any item added twice. 
- If at any point the domain of a variable is reduced to the empty set, we return a failure so that the algorithm knows to backtrack. 
- If the domain of a variable was changed, we add all the arcs from it's neighbors back to it to the queue so that the consequences these changes have will be reflected in the new domains. 
```
def MAC3(self, domains, assigned_variable):
        Initialize a queue for consistency checks
        add all of the arcs from the neighbors of the variable to that variable
            if the neighbor isn't in the assignment already:
                add the tuple of the arc from neighbor to variable as a tuple
        while there are still items in the queue:
            get the next variable assignment from the queue
            if the neighbor's domain was changed
                if the domain is now empty after the change, return failure
                otherwise, loop thorugh the neighbors, adding them to the queue to be edited as well
                    if the neighbor is not assigned (this includes assigned_variable):
                        add it to the queue
        return True
```
### Revise: 

This is the helper function for the `MAC-3` Algorithm. When this is called on all of the arcs from the neighbors of the assigned variable to the assigned variable, the domain of the assigned variable is set to be just one value (the one that we assign). Therefore, the first time that we call the revise function, it functionally checks if each value in the domain of the neighbor is consistent with the value of the assigned variable, pruning it if not. 

However, when a revision occurs and then we visit the arcs from the neighbors of the original neighbor to that original neighbor, there can be multiple values in the domain. Therefore, we just enforce arc consistency: for every value in the domain of the neighbor's neighbor, there must be at least one value in the original neighbor's domain that satisfies the constraint. This is a bit complicated to explain in words, so drawing this out helped me understand it more easily. 

This function specifically caused some confusion, because I had to distinguish between arc consistency and assignent consistency, while only using the problem class's methods to allow for different types of problems. Accordingly, I made sure that the `is_consistent` method could be used for both arc consistency and assignment consistency. The method just checks to make sure that the variable value assignment (taken as props) is consistent with the given assignment dictionary. Thus, we can just pass an `assignment` dictionary that has only the variable-value that we want to check, and do this repeatedly to enforce arc consistency. 

We use a boolean `consistent` that is initialized to `False` before we loop through the domain values of the second variable in the arc, which will be changed to true if at least one of those variables satisfies the constriants. We also break the loop if this happens-- we only need to find one value that satisfies the constriants. 
```
def revise(self, domains, neighbor, assigned_variable):
    initialize to false
    make a copy of the neghbor values
    for each value in the domain of the neighbor (D_i)
        initialize bool consistent to false
        for each value in the domain of the variable
            if that variable doesn't satisfy the constraint
                consistent = True
                break
        if not consistent:
            Remove inconsistent values from the domain
            set revised to true
    return revised
```

### New Methods Needed for Inference: 

For the implementation of inference, I had to add a new method: 

- `get_neighbors` - this returns a list of the variables that share a constraint with the input variable - used for initializing the queue in `MAC3` and for updating the queue after revisions are made. 

The main modifications had to do with retrieving the domain values for different variables and maintaining the domain copies correctly. This took some time and debugging because there were some issues with passing references, which then created incorrectly edited domains. 

## Map Coloring Implementation

The map coloring problem is pretty simple. The `variables` are the different countries in the map that need to be colored, each country's domain is comprised of all the possible colors it could be (r, g, or b, in this case), and the only constraint is that no two countries that are adjacent to one another can be the same color. 

Since the only thing that matters is what I return to the `CSP` solving class via the problem class (`MapColoringProblem.py`) methods, it doesn't really matter what I decide to put in the constructor or what I decide to name it. In this case though, it made sense to just set up the constructor as follows:
```
class MapColoringProblem:
    def __init__(self, countries, colors, adjacency):
        self.variables = countries
        self.constraints = adjacency
        self.domains = {self.variables[i]: copy.deepcopy(colors) for i in range(len(self.variables))}
```
In this case, the countries are the `variables`, the adjacency map of the countries are the constraints, and the domains are the same for all countries: `[r, g, b]`. 

### Discussion of method implementation: 

- `get_variables(self)`: since the countries are stored in a list in `self.variables`, we just return it. 

- `get_domains(self, domains=None, variable=None)`: if no `domains` dictionary and `variable` are given, just return the `self.domains` dict. This was simple, because I already initialized the dict to associate each `country` key with the list `['r', 'g', 'b']. If the `domains` dictionary is specified and a `variable` is given, then we just return the value associated with that variable's key in the dictionary. 

- `get_neighbors(self, variable)`: This was also straightforward here: the constriants of the problem is just an adjacency dictionary, so we just return the value associated with that variable key in the dictionary. 

- `choose_next_variable(self, assignment, domains)`: without the heuristic, this just iterates through the `self.variables` list until it finds a variable that isn't in the assignment, and returns that. 

- `is_consistent(self, assignment, variable, value)`: We loop through each of the countries in the adjacency list of the given variable. If that country is in the assignment and has the same value, we return `False`.

## Circuit Board Implementation

The circuitboard implementation is of course pretty similar to the map coloring implementation. I used the same methods discussed, making only the minor changes below. 

The main thing that had to be changed in the circuitboard problem was handling the overlap between components and the fact that all components could be adjacent. Because of this, I don't even store an adjacency list-- I just use the methods to return all of the other components when this is needed. 

Also, I had to find a way to store the sizes of each component in addition to the name. I just used a dictionary for this-- which doesn't matter in comparison to using just a list for the variables, becuase (once again), the methods handle everything. Thus, my `self.variables` stores each component's name and associates it with a tuple holding the width and height of the component. 

### Discussion of Method Implementation
- `get_component_domain`: This method was needed early on in the problem solving process: instead of just having a set list of colors like before, the circuit board problem requires us to find the unique domain of each component. I just do this by finding all the bottom-left coordinates for the component that don't cause it to go off the board. 
- `get_domains`: This method is pretty similar to before: if this is the first call, we construct the dictionary by adding each component and then calling `self.get_component_domain` on it to retrieve its possible values.
- `get_neighbors`: This is also about the same- since all components could overlap with one another and need to not overlap, the constraints apply to all components. Therefore, we just add every component but that component itself to each component's adjacency list. 
- `choose_next_variable`: Like before, with no heuristic, we just find the next unassigned variable. 
- `is_consistent`: This was the hardest method to write for this class, becuase we have to loop through each rectangle and make sure that it doesn't overlap with any other rectangles. This took some time to figure out, but ultimately loops through the components, checking first for any x overlap and then for any y overlap. 
- `board_to_string`: This method was just used to allow me to print the solutions and make it easier to check if they are valid. 


## Implementation of Heuristics

I won't go into the problem-specific implementation details for each of the heuristics- this can be found in the code and comments. Instead, I explain the general approach and pseudocode for each heuristic. 

To toggle the heuristics, I pass boolean values for the strategies to the constructor. The heuristics are conditionally applied accordingly. 

### MRV 

The aim of the minimum values remaining heuristic is to efficiently select which variable to assign next by choosing the variable with the smallest amount of values remaining in its domain. The logic is that, by assigning variables with less values left in their domain, we reduce the risk of having to backtrack. 

This is implemented in the `choose_next_variable` function in both problems. 

Pseudocode: 
```
remember the lowest value and which variable it is associated with
    loop through the domains of each variable
        if the variable has less values than the current min and isn't in the assignment
            udpate the min and variable
    return whichever item has the fewest remaining values
```

### DEG

The goal of the degree heuristic is to first assign the variable that is involved with the most other variables, in hopes of reducing the chance of a backtrack. This is useless in the circuitboard problem-- every piece has identical adjacency and therefore an identical degree, so I didn't even bother with implementing it. 

However, this does come in very handy on the map coloring problem, where states have varying degrees. 

This is also applied in the `choose_next_variable` method. This is used in place of the MRV, if enabled. 

Pseudo: 
```
remember the highest degree variable and the current highest degree
loop through the adjacency list of the variable in question
    if the variable has a higher degree than the current and isn't assigned
    update the highest degree and highest degree variable
return the highest degree variable
```

### LCV

This heuristic is slightly different than the others. It works within the `get_domains` method (which returns the ordered list of which values to search next) rather than in the step where we choose what variable to assign next. 

The aim here is to find the variable that reduces the domains of other variables the least. Thus, the approach is to try each variable, counting how much it reduces the domain of the other variables. Then, we return the variable that has the least repercussions for the domains of other variables. 

Pseudo: 
```
store the list of tuples containing values with their numbers of eliminations
loop through each value of the variable's domain
    remember how many values of other variables it eliminates
    for each neighbor of that variable
        if it eliminates a value in the domain of that neighbor
            increment 
    Store the variable along with the number of eliminated values as a tuple
Sort the list of tuples based on the second element (values_eliminated) in ascending order 
Extract the sorted variables from the sorted list of tuples
Return the sorted list of variables
```

## Testing: 
Again-- see the `MapColoringProblem.py` and the `CirctuitBoardProblem.py` for the tests themselves and output. Methods are discussed below.

All of the methods discussed for the implementation of each problem were tested invididually throughout. I don't discuss all of those here- it doesn't matter. 

As for backtracking and inference, I did trace through the entire coloring problem and most of the circuitboard problem using print statements to make sure that the recursive calls were occurring correctly. It took some debugging but I did figure this out. 

I got this all working before even moving on to heuristics, which took much more time to test, becuase I had to construct a bunch of different problems to test each heuristic with and without inference. 

Before moving on to runtime, I ran each heuristic on the problem using print statements to debug and ensure that the heuristics were working as intended. By having the problems print out the domains at different points right before seleting the next variable or domain value to test, I was able to confirm that all the heuristics were working correctly. 

At this point, I had checked all of the solutions outputted by my algorithms, and all were valid, so I was focusing more on the runtime of each heuristic. 

I imported python's `time` class, saving the time before each call to the problem solver and then subtracting it from the time after the result was found to calculate runtime. 

Here are the results for the map coloring. I've cut out the solutions themselves because it cluttered this report up way too much, but running the `MapColoringProblem.py` file will print the full outputs. 
```
No Inference No Heuristics Runtime: 1.3113021850585938e-05 seconds
No Inference with MRV Runtime: 1.0013580322265625e-05 seconds
No Inference with DEG Runtime: 7.867813110351562e-06 seconds
No Inference with LCV Runtime: 2.6702880859375e-05 seconds
No Inference with MRV and LCV Runtime: 1.3828277587890625e-05 seconds
No Inference with DEG and LCV Runtime: 1.430511474609375e-05 seconds
Inference with No Heuristics Runtime: 0.00010704994201660156 seconds
Inference with MRV Runtime: 9.584426879882812e-05 seconds
Inference with DEG Runtime: 8.606910705566406e-05 seconds
Inference with LCV Runtime: 0.00017189979553222656 seconds
Inference with MRV and LCV Runtime: 0.0001709461212158203 seconds
Inference with DEG and LCV Runtime: 0.0001399517059326172 seconds
```
On the map problem, We see that inference is a fair bit slower-- as discussed in the textbook, inference doesn't help out much here. 

The heuristics help more without inference, because they are called less times and can't clutter up the process as much. Without inference, all heuristics reduce the runtime except for LCV. Since constraints can only reduce the domain of another by one here, there isn't much effect. The degree heuristic reduces runtime here by almost 50% though, which is pretty good. MRV reduces it as well, but not by much. 

The same process is done for the Circuit board problem. See `CircuitBoardProblem.py` for the full diagrams printed out. (Notice the degree heuristic doesn't help here so it isn't implemented or tested)
```
No Inference No Heuristics Runtime: 2.4080276489257812e-05 seconds
No Inference MRV Runtime: 1.811981201171875e-05 seconds
No Inference LCV Runtime: 0.00012803077697753906 seconds
No Inference MRV LCV Runtime: 4.482269287109375e-05 seconds
Inference No Heuristic Runtime: 0.00021886825561523438 seconds
Inference MRV Runtime: 0.00019407272338867188 seconds
Inference LCV Runtime: 0.0007181167602539062 seconds
Inference MRV LCV Runtime: 0.0006630420684814453 seconds
```
As shown above, inference was much less effective in this problem, due to the increased number of constraint relationships and domain values. 
MRV was the most effective heuristic here, but it was actually the only one that decreased runtime. Runtimes weren't drastically affected, but of course this is a small problem and most of the runtimes are still in the ten-thousandths of a second range. 

## Extra Credit: 

The Degree heuristic was not too difficult to implement, but did take some extra time. I describe its design and implementation above with the other heuristics. 

I took the time to construct an alternative, larger map coloring problem: the United States. I read about this online and found out that the chromatic number for the United States map is 4: so I created an alternative problem initialization that has the adjacency list of the United States, with every state as a variable and the color set `[r, g, b, y]`. You can test this too: just uncomment the variables with the United States info and comment out the Australia ones (I didn't change the names because setting up all the different problems took forever, and this is way easier for both of us). 

I ran all of the runtime tests and found the following results (these are copied in the comments at the bottom of `MapColoringProblem.py` with the actual assignments included):
``` 
No Inference No Heuristics Runtime: 16.84667181968689 seconds
No Inference with MRV Runtime: 21.745162963867188 seconds
No Inference with DEG Runtime: 0.00015997886657714844 seconds
No Inference with LCV Runtime: 34.742955923080444 seconds
No Inference with MRV and LCV Runtime: 39.77112007141113 seconds
No Inference with DEG and LCV Runtime: 0.00026297569274902344 seconds
Inference with No Heuristics Runtime: 86.06060576438904 seconds
Inference with MRV Runtime: 0.005126953125 seconds
Inference with DEG Runtime: 0.0032498836517333984 seconds
Inference with LCV Runtime: 0.0055332183837890625 seconds
Inference with MRV and LCV Runtime: 0.008306026458740234 seconds
Inference with DEG and LCV Runtime: 0.004997968673706055 seconds
```

With a much larger set, the runtimes are much greater. However, the heuristics made a massive impact. 

Here are some of my observations: 

The degree heuristic was by far the most effective, as with the australia problem. However, in this case, it was over 100,000 times faster than the normal backtracking. Again, the MRV and LCV heuristics are better fit to more highly constrained problems, unlike this one. 

Inference also began to make a huge difference: pruning the domain was a massive influence on the runtime. All of the problems that used inference and a heuristic managed to find a solution in less than one hundredth of a second, while the backtracking without inference or the degree heuristic ended up near half a minute of runtime. 

Most interestingly though-- the inference on its own with no heuristics took nearly a minute and a half. The addition of these heuristics then cut all of the times down by an incredible factor. 

All of the problems found valid solutions, which was good to confirm, of course. 