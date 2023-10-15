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

I began with these methods to do so: 
- `is_assignment_complete`
- `get_variables`
- `get_domains`
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

This has a much greater effect on other problems though (like the circuitboard problem), and can even solve them outright in some instances. 

I designed the algorithm according to the above logic with help from the textbook: we do backtracking normally, but at at each new assignment, we prune the domains of the remaining variables to reduce search time. 

What if the inference algorithm finds that this assignment leads to no solution though? Of course, we backtrack, but we have to be able to revert to the old, un-pruned domains. Additionally,Accordingly, we must maintain both the pruned domain and the original domain, which I did by using python's `deepcopy` method to create a version of the domains dictionary that would allow me to change it without affecting the original copy. That way, if a dead end is encountered, we can just remove the most recent assignment and carry on with the normal path. 

Below is the pseudo for all three methods: 


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
## Map Coloring Implementation
The map coloring problem is pretty simple. The `variables` are the different countries in the map that need to be colored, each country's domain is comprised of all the possible colors it could be (r, g, or b, in this case), and the only constraint is that no two countries that are adjacent to one another can be the same color. 
