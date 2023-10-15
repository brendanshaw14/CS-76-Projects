# CSP Report

This report discusses the design, implementation, and testing processes of the CSP project.

## General structure

Since we were not given any provided code, I began by deciding what information to store in which class. This was a little bit difficult at first, but I ultimately decided to have two components to the problem representation and solving: the `CSP.py` class for solving logic and then a class to represent each problem. I tried to store as much information and problem logic in the problem classes as possible, becuase this allows for more flexibility specific to each problem. 

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

- `choose_next_variable(self, assignment)`: without the heuristic, this just iterates through the `self.variables` list until it finds a variable that isn't in the assignment, and returns that. 

- `is_consistent(self, assignment, variable, value)`: We loop through each of the countries in the adjacency list of the given variable. If that country is in the assignment and has the same value, we return `False`.
